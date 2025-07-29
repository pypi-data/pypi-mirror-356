# canonmap/services/artifact_unpacker/artifact_unpacker.py

import pickle
import json
from pathlib import Path
import pandas as pd
import logging

from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.utils.logger import get_logger
import logging

logger = get_logger("artifact_unpacker")

class ArtifactUnpacker:
    """
    Reverse of ArtifactGenerator: reads .pkl artifacts and emits JSON/CSV.
    """

    def unpack_artifacts(self, request: ArtifactUnpackingRequest) -> None:
        """
        Read any *_canonical_entities.pkl, *_schema.pkl, and *_processed_data.pkl
        files in the first layer of `request.input_path` and export them as JSON/CSV
        into `request.output_path` (or back to `request.input_path` if output_path is None).
        """
        in_dir = Path(request.input_path)
        out_dir = Path(request.output_path) if request.output_path else in_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) canonical entities → JSON
        for pkl in in_dir.glob("*_canonical_entities.pkl"):
            data = pickle.load(pkl.open("rb"))
            target = out_dir / f"{pkl.stem}.json"
            with target.open("w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Unpacked {pkl.name} → {target.name}")

        # 2) schema → JSON
        for pkl in in_dir.glob("*_schema.pkl"):
            data = pickle.load(pkl.open("rb"))
            target = out_dir / f"{pkl.stem}.json"
            with target.open("w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Unpacked {pkl.name} → {target.name}")

        # 3) processed data → CSV (or fallback JSON)
        for pkl in in_dir.glob("*_processed_data.pkl"):
            obj = pd.read_pickle(pkl)
            if isinstance(obj, dict) and "tables" in obj:
                # combined: one CSV per table
                for tbl, df in obj["tables"].items():
                    csv_file = out_dir / f"{tbl}.csv"
                    df.to_csv(csv_file, index=False)
                    logger.info(f"Unpacked {pkl.name}[{tbl}] → {csv_file.name}")
            elif isinstance(obj, pd.DataFrame):
                # single-table processed data
                csv_file = out_dir / f"{pkl.stem}.csv"
                obj.to_csv(csv_file, index=False)
                logger.info(f"Unpacked {pkl.name} → {csv_file.name}")
            else:
                # some other structure: write JSON
                target = out_dir / f"{pkl.stem}.json"
                with target.open("w") as f:
                    json.dump(obj, f, indent=2)
                logger.info(f"Unpacked {pkl.name} → {target.name}")

        # reset logging to debug before returning
        logger.setLevel(logging.DEBUG)