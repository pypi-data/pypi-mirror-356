# File: canonmap/services/artifact_unpacker/artifact_unpacker.py

import pickle
import json
from pathlib import Path
import pandas as pd
import logging
from typing import Optional, Dict

from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.utils.logger import get_logger

logger = get_logger("artifact_unpacker")

class ArtifactUnpacker:
    """
    Reads .pkl artifacts from a preloaded artifact_files dict
    and exports them as JSON/CSV into request.output_path.
    """
    def __init__(self, artifact_files: Optional[Dict[str, Path]] = None):
        # artifact_files comes from your Controller's find_artifact_files()
        self.artifact_files = artifact_files or {}

    def unpack_artifacts(self, request: ArtifactUnpackingRequest) -> Dict[str, Path]:
        out_dir = Path(request.output_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        results: Dict[str, Path] = {}

        # 1) canonical entities → JSON
        pkl = self.artifact_files.get("canonical_entities")
        if pkl:
            data = pickle.load(pkl.open("rb"))
            target = out_dir / f"{pkl.stem}.json"
            with target.open("w") as f:
                json.dump(data, f, indent=2)
            results["canonical_entities"] = target
            logger.info(f"Unpacked {pkl.name} → {target.name}")

        # 2) schema → JSON
        pkl = self.artifact_files.get("schema")
        if pkl:
            data = pickle.load(pkl.open("rb"))
            target = out_dir / f"{pkl.stem}.json"
            with target.open("w") as f:
                json.dump(data, f, indent=2)
            results["schema"] = target
            logger.info(f"Unpacked {pkl.name} → {target.name}")

        # 3) processed data → CSV or JSON
        pkl = self.artifact_files.get("processed_data")
        if pkl:
            obj = pd.read_pickle(pkl)
            if isinstance(obj, dict) and "tables" in obj:
                # combined: one CSV per table
                for tbl, df in obj["tables"].items():
                    csv_file = out_dir / f"{tbl}.csv"
                    df.to_csv(csv_file, index=False)
                    results[f"processed_data_{tbl}"] = csv_file
                    logger.info(f"Unpacked {pkl.name}[{tbl}] → {csv_file.name}")
            elif isinstance(obj, pd.DataFrame):
                # single-table processed data
                csv_file = out_dir / f"{pkl.stem}.csv"
                obj.to_csv(csv_file, index=False)
                results["processed_data"] = csv_file
                logger.info(f"Unpacked {pkl.name} → {csv_file.name}")
            else:
                # fallback JSON output
                target = out_dir / f"{pkl.stem}.json"
                with target.open("w") as f:
                    json.dump(obj, f, indent=2)
                results["processed_data_json"] = target
                logger.info(f"Unpacked {pkl.name} → {target.name}")

        if request.verbose:
            logger.setLevel(logging.DEBUG)

        return results