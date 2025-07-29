# canonmap/services/artifact_generator/pipeline.py

"""Pipeline for generating artifacts from input data."""

import json
import os
import pickle
import time
from pathlib import Path
from typing import Any, Dict, Optional
import logging

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_generation_response import ArtifactGenerationResponse
from canonmap.services.artifact_generator.entities.canonical_entities_generator import (
    generate_canonical_entities,
)
from canonmap.services.artifact_generator.ingestion.clean_columns import clean_and_format_columns
from canonmap.services.artifact_generator.ingestion.convert_input import convert_data_to_df
from canonmap.services.artifact_generator.schema.db_types.mariadb.generate_mariadb_loader_script import (
    generate_mariadb_loader_script,
)
from canonmap.services.artifact_generator.schema.infer_schema import generate_db_schema_from_df
from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.utils.logger import get_logger

load_dotenv()
DEV = os.getenv("DEV", "false").lower() == "true"
logger = get_logger()


def run_artifact_generation_pipeline(
    config: ArtifactGenerationRequest,
    embedder: Optional[Any] = None,
    nlp: Optional[Any] = None,
) -> ArtifactGenerationResponse:
    output_dir = Path(config.output_path or "./canonmap_output")
    output_dir.mkdir(parents=True, exist_ok=True)

    def stage(label: str):
        t0 = time.time()

        def done():
            logger.info(f"⏱️ {label} took {round(time.time() - t0, 2)}s")

        return t0, done

    pipeline_start = time.time()
    logger.info("Starting artifact generation pipeline...")

    # --- ingest ---
    if isinstance(config.input_path, str) and Path(config.input_path).is_dir():
        logger.info(f"Directory input detected at '{config.input_path}'")
        if not config.file_pattern:
            logger.warning("⚠️ A 'file_pattern' must be provided when passing a directory.")
        else:
            logger.info(f"Using file pattern '{config.file_pattern}' to match files.")

    t0, done = stage("Data ingestion")
    tables = convert_data_to_df(
        config.input_path, config.num_rows, config.recursive, config.file_pattern
    )
    done()

    # If a single DataFrame was returned, turn it into {table_name: df},
    # deriving table_name from the filename when not provided.
    if isinstance(tables, pd.DataFrame):
        if not config.table_name:
            if isinstance(config.input_path, str):
                path = Path(config.input_path)
                if path.is_file():
                    stem = path.stem
                else:
                    stem = "data"
            else:
                stem = "data"
            # normalize: lowercase, strip, replace spaces with underscores
            config.table_name = stem.lower().strip().replace(" ", "_")
        tables = {config.table_name: tables}

    result_paths: Dict[str, Dict[str, Path]] = {}
    entity_map: Dict[str, Any] = {}
    embedding_map: Dict[str, np.ndarray] = {}
    embedding_jobs: Any = []

    # --- per-table processing ---
    for name, df in tables.items():
        t0, done = stage(f"Process table: {name}")
        local_cfg = config.model_copy(deep=True)
        local_cfg.table_name = name

        paths = _get_paths(
            output_dir, config.source_name, name, config.schema_database_type
        )
        result_paths[name], entities, embedding_strings = _process_table(
            df, local_cfg, paths, nlp
        )
        entity_map[name] = entities

        if config.generate_embeddings:
            embedding_jobs.append((name, embedding_strings))

        done()

    # --- embedding ---
    if config.generate_embeddings and embedder:
        logger.info(f"Embedding canonical entities for {len(embedding_jobs)} tables…")
        t0, done = stage("Embedding canonical entities")

        # one-shot encode all jobs
        embedding_map = embedder.embed_texts(embedding_jobs)

        done()

        # write out per-table embeddings
        for table_name, arr in embedding_map.items():
            emb_path = result_paths[table_name]["canonical_entity_embeddings"]
            np.savez_compressed(emb_path, embeddings=arr)
            if DEV:
                logger.info(f"Saved embeddings for '{table_name}' to {emb_path}")

    # --- combined (multi-table) artifacts ---
    if len(tables) > 1:
        t0, done = stage("Write combined artifacts")
        result_paths[config.source_name] = _write_combined_artifacts(
            config, output_dir, entity_map, embedding_map, tables
        )
        done()

    total_time = round(time.time() - pipeline_start, 2)
    logger.info(f"Artifact generation pipeline finished in {total_time}s")

    # reset logging to debug before returning
    logger.setLevel(logging.DEBUG)

    return ArtifactGenerationResponse(
        message=f"Artifacts generated for {len(tables)} table(s)",
        paths={k: {kk: str(vv) for kk, vv in v.items()} for k, v in result_paths.items()},
        statistics={
            "total_tables": len(tables),
            "total_entities": sum(len(v) for v in entity_map.values()),
            "total_embeddings": sum(len(v) for v in embedding_map.values())
            if embedding_map
            else 0,
            "tables_processed": list(tables.keys()),
        },
    )


def _process_table(df, config, paths, nlp):
    # 1) Clean field names (if requested) and ensure uniqueness
    if config.clean_field_names:
        df = clean_and_format_columns(df)

        # If any column names collided, append _1, _2, ... to duplicates
        if df.columns.duplicated().any():
            seen: dict[str, int] = {}
            new_cols: list[str] = []
            for col in df.columns:
                if col not in seen:
                    seen[col] = 0
                    new_cols.append(col)
                else:
                    seen[col] += 1
                    new_cols.append(f"{col}_{seen[col]}")
            df.columns = new_cols

    # 2) Generate schema for this table
    schema: Dict[str, Any] = {}
    if config.generate_schema:
        schema = {
            config.source_name: {
                config.table_name: generate_db_schema_from_df(
                    df,
                    config.schema_database_type,
                    config.clean_field_names
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

    # 3) Save processed DataFrame (if requested)
    if config.save_processed_data:
        df.to_pickle(paths["processed_data"])

    # 4) Generate canonical entities and prepare strings for embedding
    entities = []
    embedding_strings: Any = []
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
            embedding_strings = [
                json.dumps({e["_field_name_"]: e["_canonical_entity_"]})
                for e in entities
            ]

    # 5) Write the per-table loader script (if schema was generated)
    if config.generate_schema:
        script = generate_mariadb_loader_script(
            schema[config.source_name][config.table_name],
            config.table_name,
            str(paths["data_loader_script"]),
        )
        paths["data_loader_script"].write_text(script)

    return paths, entities, embedding_strings




def _write_combined_artifacts(
    config, output_path: Path, entities: Any, embeddings: Dict[str, np.ndarray], tables: Dict[str, pd.DataFrame]
) -> Dict[str, Path]:
    """
    Writes out the combined artifacts for multi-table pipelines,
    but only includes each artifact when its corresponding flag is True.
    """
    combined: Dict[str, Path] = {}

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

    if config.generate_canonical_entities:
        ents_path = output_path / f"{config.source_name}_canonical_entities.pkl"
        with open(ents_path, "wb") as f:
            pickle.dump(entities, f)
        if DEV:
            json_path = ents_path.with_suffix(".json")
            with open(json_path, "w") as f:
                json.dump(entities, f, indent=4)
            logger.info(f"Saved combined canonical entities to {json_path}")
        combined["canonical_entities"] = ents_path

    if config.generate_embeddings and embeddings:
        emb_path = output_path / f"{config.source_name}_canonical_entity_embeddings.npz"
        np.savez_compressed(emb_path, **embeddings)
        combined["canonical_entity_embeddings"] = emb_path

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
    dir = base / table
    dir.mkdir(parents=True, exist_ok=True)
    return {
        "schema": dir / f"{source}_{table}_schema.pkl",
        "processed_data": dir / f"{source}_{table}_processed_data.pkl",
        "canonical_entities": dir / f"{source}_{table}_canonical_entities.pkl",
        "canonical_entity_embeddings": dir
        / f"{source}_{table}_canonical_entity_embeddings.npz",
        "data_loader_script": dir
        / f"load_{table}_table_to_{db_type}.py",
    }