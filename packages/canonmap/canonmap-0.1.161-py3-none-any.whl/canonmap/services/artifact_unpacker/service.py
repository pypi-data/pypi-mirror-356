# canonmap/services/artifact_unpacker/service.py

import pickle
import json
import logging
from pathlib import Path
from typing import Dict

import pandas as pd

from canonmap import ArtifactUnpackingRequest
from canonmap.utils.logger import get_logger

logger = get_logger("artifact_unpacker")


class ArtifactUnpacker:
    """
    Reads .pkl artifacts from a provided artifact_files dict
    and exports them as JSON/CSV into request.output_path.
    """

    def __init__(self, artifact_files: Dict[str, Path]) -> None:
        self.artifact_files = artifact_files

    def unpack_artifacts(self, request: ArtifactUnpackingRequest) -> Dict[str, Path]:
        if request.verbose:
            logger.setLevel(logging.DEBUG)
            
        out_dir = Path(request.output_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        results: Dict[str, Path] = {}

        # canonical_entities → JSON
        pkl = self.artifact_files.get("canonical_entities")
        if pkl:
            data = pickle.load(pkl.open("rb"))
            tgt = out_dir / f"{pkl.stem}.json"
            with tgt.open("w") as f:
                json.dump(data, f, indent=2)
            results["canonical_entities"] = tgt
            logger.info(f"Unpacked {pkl.name} → {tgt.name}")

        # schema → JSON
        pkl = self.artifact_files.get("schema")
        if pkl:
            data = pickle.load(pkl.open("rb"))
            tgt = out_dir / f"{pkl.stem}.json"
            with tgt.open("w") as f:
                json.dump(data, f, indent=2)
            results["schema"] = tgt
            logger.info(f"Unpacked {pkl.name} → {tgt.name}")

        # processed_data → CSV or JSON
        pkl = self.artifact_files.get("processed_data")
        if pkl:
            try:
                obj = pd.read_pickle(pkl)
                if isinstance(obj, dict) and "tables" in obj:
                    for tbl, df in obj["tables"].items():
                        csvf = out_dir / f"{tbl}.csv"
                        df.to_csv(csvf, index=False)
                        results[f"processed_data_{tbl}"] = csvf
                        logger.info(f"Unpacked {pkl.name}[{tbl}] → {csvf.name}")
                elif isinstance(obj, pd.DataFrame):
                    csvf = out_dir / f"{pkl.stem}.csv"
                    obj.to_csv(csvf, index=False)
                    results["processed_data"] = csvf
                    logger.info(f"Unpacked {pkl.name} → {csvf.name}")
                else:
                    tgt = out_dir / f"{pkl.stem}.json"
                    with tgt.open("w") as f:
                        json.dump(obj, f, indent=2)
                    results["processed_data_json"] = tgt
                    logger.info(f"Unpacked {pkl.name} → {tgt.name}")
            except Exception as e:
                logger.error(f"Error unpacking processed data: {e}", exc_info=True)

        # semantic_texts → Unzip to semantic_txts/<table_name>/
        zip_path = self.artifact_files.get("semantic_texts")
        if zip_path:
            import zipfile
            semantic_dir = out_dir / "semantic_txts"
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                for member in zipf.namelist():
                    # Expecting filenames like table_name_row_idx_field.txt
                    parts = member.split('_row_')
                    if len(parts) > 1:
                        table_name = parts[0]
                    else:
                        table_name = "unknown"
                    table_dir = semantic_dir / table_name
                    table_dir.mkdir(parents=True, exist_ok=True)
                    tgt_path = table_dir / member
                    with tgt_path.open('wb') as f:
                        f.write(zipf.read(member))
            results["semantic_texts"] = semantic_dir
            logger.info(f"Unpacked {zip_path.name} → {semantic_dir}")

        return results