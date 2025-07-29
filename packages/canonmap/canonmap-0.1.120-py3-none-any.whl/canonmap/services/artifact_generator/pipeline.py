# canonmap/services/artifact_generator/pipeline.py

"""Pipeline for generating artifacts from input data."""

import json
import os
import pickle
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_generation_response import ArtifactGenerationResponse
from canonmap.services.artifact_generator.entities.canonical_entities_generator import (
    generate_canonical_entities,
)
from canonmap.services.artifact_generator.ingestion.clean_columns import (
    clean_and_format_columns,
)
from canonmap.services.artifact_generator.ingestion.convert_input import convert_data_to_df
from canonmap.services.artifact_generator.schema.db_types.mariadb.generate_mariadb_loader_script import (
    generate_mariadb_loader_script,
)
from canonmap.services.artifact_generator.schema.infer_schema import (
    generate_db_schema_from_df,
)
from canonmap.utils.logger import get_logger

load_dotenv()
DEV = os.getenv("DEV", "false").lower() == "true"
logger = get_logger("artifact_generation_pipeline")


def _normalize(name: str) -> str:
    """Lowercase, strip, and replace spaces with underscores."""
    return name.lower().strip().replace(" ", "_")


def run_artifact_generation_pipeline(
    config: ArtifactGenerationRequest,
    embedder: Optional[Any] = None,
    nlp: Optional[Any] = None,
) -> ArtifactGenerationResponse:
    output_dir = Path(config.output_path or "./canonmap_output")
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting artifact generation pipeline...")

    # 1) ingest
    if isinstance(config.input_path, str) and Path(config.input_path).is_dir():
        logger.info(f"Directory input detected at '{config.input_path}'")
        if not config.file_pattern:
            logger.warning("A 'file_pattern' must be provided when passing a directory.")
        else:
            logger.info(f"Using file pattern '{config.file_pattern}' to match files.")

    tables = convert_data_to_df(
        config.input_path, config.num_rows, config.recursive, config.file_pattern
    )

    # 2) wrap single DataFrame in a dict
    if isinstance(tables, pd.DataFrame):
        if isinstance(config.input_path, str) and Path(config.input_path).is_file():
            raw = Path(config.input_path).stem
        else:
            raw = config.table_name or "data"
        tables = {raw: tables}

    is_multi = len(tables) > 1

    # 3) optionally normalize all table names and entity_fields
    if config.normalize_table_names:
        normalized: Dict[str, pd.DataFrame] = {}
        for raw_name, df in tables.items():
            norm = _normalize(raw_name)
            normalized[norm] = df
        tables = normalized

        if config.entity_fields:
            for ef in config.entity_fields:
                ef.table_name = _normalize(ef.table_name)

    result_paths: Dict[str, Dict[str, Path]] = {}
    entity_map: Dict[str, list[dict]] = {}
    embedding_jobs: list[tuple[str, list[str]]] = []

    # 4) per-table processing
    for table_name, df in tables.items():
        logger.info(f"Processing table: {table_name}")
        local_cfg = config.model_copy(deep=True)
        local_cfg.table_name = table_name

        base_dir = output_dir / table_name if is_multi else output_dir
        paths = _get_paths(
            base_dir, config.source_name, table_name, config.schema_database_type
        )

        paths, entities, emb_strs = _process_table(df, local_cfg, paths, nlp)
        result_paths[table_name] = paths
        entity_map[table_name] = entities

        if config.generate_embeddings:
            embedding_jobs.append((table_name, emb_strs))

    # 5) embeddings (parallel per-table for speed)
    embedding_map: Dict[str, np.ndarray] = {}
    if config.generate_embeddings and embedder:
        logger.info(f"Embedding canonical entities for {len(embedding_jobs)} tables…")
        # returns { table_name: np.ndarray }
        embedding_map = embedder.embed_texts(embedding_jobs)

        # write per-table embeddings (optional)
        for tbl, arr in embedding_map.items():
            emb_path = result_paths[tbl]["canonical_entity_embeddings"]
            np.savez_compressed(emb_path, embeddings=arr)
            if DEV:
                logger.info(f"Saved embeddings for '{tbl}' to {emb_path}")

    # 6) combined (multi-table) artifacts
    if is_multi:
        logger.info("Writing combined artifacts…")
        result_paths[config.source_name] = _write_combined_artifacts(
            config, output_dir, entity_map, embedding_map, tables
        )

    # single-table: still write combined artifacts under table_name key?
    # (if you wish, you can skip combined for single)

    logger.info("Artifact generation pipeline finished")
    return ArtifactGenerationResponse(
        message=f"Artifacts generated for {len(tables)} table(s)",
        paths={k: {kk: str(vv) for kk, vv in v.items()} for k, v in result_paths.items()},
        statistics={
            "total_tables": len(tables),
            "total_entities": sum(len(v) for v in entity_map.values()),
            "total_embeddings": (
                sum(arr.shape[0] for arr in embedding_map.values())
                if embedding_map
                else 0
            ),
            "tables_processed": list(tables.keys()),
        },
    )


def _process_table(df, config, paths, nlp):
    # 1) Clean field names and dedupe
    if config.clean_field_names:
        df = clean_and_format_columns(df)
        if df.columns.duplicated().any():
            seen: Dict[str, int] = {}
            new_cols: list[str] = []
            for col in df.columns:
                seen[col] = seen.get(col, 0)
                new_cols.append(col if seen[col] == 0 else f"{col}_{seen[col]}")
                seen[col] += 1
            df.columns = new_cols

    # 2) Schema
    schema: Dict[str, Any] = {}
    if config.generate_schema:
        schema = {
            config.source_name: {
                config.table_name: generate_db_schema_from_df(
                    df, config.schema_database_type, config.clean_field_names
                )
            }
        }
        with open(paths["schema"], "wb") as f:
            pickle.dump(schema, f)
        if DEV:
            json_path = paths["schema"].with_suffix(".json")
            with open(json_path, "w") as f:
                json.dump(schema, f, indent=4)
            logger.info(f"Saved schema for {config.table_name} to {json_path}")

    # 3) Processed data
    if config.save_processed_data:
        df.to_pickle(paths["processed_data"])

    # 4) Canonical entities + prepare embeddings
    entities: list[dict] = []
    embedding_strings: list[str] = []
    if config.generate_canonical_entities:
        entities = generate_canonical_entities(
            df,
            schema,
            config.schema_database_type,
            [
                ef.model_dump()
                for ef in (config.entity_fields or [])
                if ef.table_name == config.table_name
            ],
            config.source_name,
            config.table_name,
            config.use_other_fields_as_metadata,
            config.clean_field_names,
        )
        with open(paths["canonical_entities"], "wb") as f:
            pickle.dump(entities, f)
        if DEV:
            json_path = paths["canonical_entities"].with_suffix(".json")
            with open(json_path, "w") as f:
                json.dump(entities, f, indent=4)
            logger.info(f"Saved canonical entities for {config.table_name} to {json_path}")

        if config.generate_embeddings:
            import json as _json

            embedding_strings = [
                _json.dumps({e["_field_name_"]: e["_canonical_entity_"]})
                for e in entities
            ]

    # 5) Write loader script
    if config.generate_schema:
        script = generate_mariadb_loader_script(
            schema[config.source_name][config.table_name],
            config.table_name,
            str(paths["data_loader_script"]),
        )
        paths["data_loader_script"].write_text(script)

    return paths, entities, embedding_strings


def _write_combined_artifacts(
    config: ArtifactGenerationRequest,
    output_path: Path,
    entities: Dict[str, list[dict]],
    embeddings: Dict[str, np.ndarray],
    tables: Dict[str, pd.DataFrame],
) -> Dict[str, Path]:
    combined: Dict[str, Path] = {}

    # 1) processed_data
    if config.save_processed_data:
        processed_path = output_path / f"{config.source_name}_processed_data.pkl"
        combined_data = {
            "metadata": {"source_name": config.source_name, "tables": list(tables.keys())},
            "tables": {
                name: clean_and_format_columns(df)
                if config.clean_field_names
                else df
                for name, df in tables.items()
            },
        }
        with open(processed_path, "wb") as f:
            pickle.dump(combined_data, f)
        combined["processed_data"] = processed_path

    # 2) schema
    if config.generate_schema:
        schema = {config.source_name: {}}
        for name, df in tables.items():
            schema[config.source_name][name] = generate_db_schema_from_df(
                df, config.schema_database_type, config.clean_field_names
            )
        schema_path = output_path / f"{config.source_name}_schema.pkl"
        with open(schema_path, "wb") as f:
            pickle.dump(schema, f)
        combined["schema"] = schema_path
        if DEV:
            json_path = schema_path.with_suffix(".json")
            with open(json_path, "w") as f:
                json.dump(schema, f, indent=4)
            logger.info(f"Saved combined schema to {json_path}")

    # 3) flat canonical entities
    if config.generate_canonical_entities:
        flat_list: list[dict] = []
        for tbl in tables.keys():
            flat_list.extend(entities.get(tbl, []))

        ents_path = output_path / f"{config.source_name}_canonical_entities.pkl"
        with open(ents_path, "wb") as f:
            pickle.dump(flat_list, f)
        combined["canonical_entities"] = ents_path

        if DEV:
            json_path = ents_path.with_suffix(".json")
            with open(json_path, "w") as f:
                json.dump(flat_list, f, indent=2)
            logger.info(f"Saved flat canonical entities to {json_path}")

    # 4) flat combined embeddings
    if config.generate_embeddings and embeddings:
        # stack arrays in same table order as canonical_entities
        arrays = [embeddings[tbl] for tbl in tables.keys()]
        flat_embs = np.vstack(arrays) if arrays else np.empty((0,))

        emb_path = output_path / f"{config.source_name}_canonical_entity_embeddings.npz"
        # save under a single key "embeddings"
        np.savez_compressed(emb_path, embeddings=flat_embs)
        combined["canonical_entity_embeddings"] = emb_path

    # 5) loader script
    if config.generate_schema:
        loader_path = output_path / f"load_{config.source_name}_to_{config.schema_database_type}.py"
        script = generate_mariadb_loader_script(
            {k: v for k, v in schema[config.source_name].items()},
            list(schema[config.source_name].keys()),
            str(loader_path),
            is_combined=True,
        )
        loader_path.write_text(script)
        combined["data_loader_script"] = loader_path

    return combined


def _get_paths(
    base: Path, source: str, table: str, db_type: str
) -> Dict[str, Path]:
    """
    Returns the artifact file paths for a single table.
    'base' is already the correct directory (nested for multi, root for single).
    """
    base.mkdir(parents=True, exist_ok=True)
    return {
        "schema": base / f"{source}_{table}_schema.pkl",
        "processed_data": base / f"{source}_{table}_processed_data.pkl",
        "canonical_entities": base / f"{source}_{table}_canonical_entities.pkl",
        "canonical_entity_embeddings": base / f"{source}_{table}_canonical_entity_embeddings.npz",
        "data_loader_script": base / f"load_{table}_table_to_{db_type}.py",
    }