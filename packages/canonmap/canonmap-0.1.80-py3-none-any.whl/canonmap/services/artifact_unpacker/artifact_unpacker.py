# canonmap/services/artifact_unpacker.py

import pickle
import json
from pathlib import Path
import pandas as pd
from canonmap.utils.logger import get_logger

logger = get_logger()

class ArtifactUnpacker:
    """
    Reverse of ArtifactGenerator: reads .pkl artifacts and emits JSON/CSV.
    """

    @staticmethod
    def unpack_artifacts(
        input_path: str | Path,
        output_path: str | Path | None = None
    ) -> None:
        in_dir = Path(input_path)
        out_dir = Path(output_path) if output_path else in_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        # canonical entities → JSON
        for pkl in in_dir.glob("*_canonical_entities.pkl"):
            data = pickle.load(pkl.open("rb"))
            target = out_dir / f"{pkl.stem}.json"
            with target.open("w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Unpacked {pkl.name} → {target.name}")

        # schema → JSON
        for pkl in in_dir.glob("*_schema.pkl"):
            data = pickle.load(pkl.open("rb"))
            target = out_dir / f"{pkl.stem}.json"
            with target.open("w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Unpacked {pkl.name} → {target.name}")

        # processed data → CSV or fallback JSON
        for pkl in in_dir.glob("*_processed_data.pkl"):
            obj = pd.read_pickle(pkl)
            if isinstance(obj, dict) and "tables" in obj:
                for tbl, df in obj["tables"].items():
                    csv_file = out_dir / f"{tbl}.csv"
                    df.to_csv(csv_file, index=False)
                    logger.info(f"Unpacked {pkl.name}[{tbl}] → {csv_file.name}")
            elif isinstance(obj, pd.DataFrame):
                csv_file = out_dir / f"{pkl.stem}.csv"
                obj.to_csv(csv_file, index=False)
                logger.info(f"Unpacked {pkl.name} → {csv_file.name}")
            else:
                fallback = out_dir / f"{pkl.stem}.json"
                with fallback.open("w") as f:
                    json.dump(obj, f, indent=2)
                logger.info(f"Unpacked {pkl.name} → {fallback.name}")