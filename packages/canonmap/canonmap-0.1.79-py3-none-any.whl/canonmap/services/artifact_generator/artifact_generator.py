# canonmap/services/artifact_generator/artifact_generator.py

import logging
import time
from pathlib import Path
import pickle
import json
import pandas as pd
from typing import Optional, Dict, Any

from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.classes.embedder import Embedder
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.services.artifact_generator.pipeline import run_artifact_generation_pipeline
from canonmap.utils.get_cpu_count import get_cpu_count

logger = logging.getLogger(__name__)


class ArtifactGenerator:
    def __init__(
        self,
        config: ArtifactGenerationRequest,
        embedder: Optional[Embedder] = None,
        nlp: Optional[Any] = None,
    ) -> None:
        self.config = config
        self.embedder = embedder or Embedder(
            model_name="all-MiniLM-L6-v2",
            batch_size=1024
        )
        self.nlp = nlp or load_spacy_model()
        self.num_cores = get_cpu_count()
        logger.setLevel(logging.DEBUG if config.verbose else logging.WARNING)

    def generate_artifacts(self) -> Dict[str, Any]:
        logger.info(f"Generating artifacts with config: {self.config}")
        start = time.time()
        result = run_artifact_generation_pipeline(self.config, self.embedder, self.nlp)
        logger.info(f"⏱️ Total artifact generation time: {round(time.time() - start, 2)}s")
        return result
    

    def unpack_artifacts(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None
    ) -> None:
        """
        Read any *_canonical_entities.pkl, *_schema.pkl, and *_processed_data.pkl
        files in the first layer of `input_path` and export them as JSON/CSV
        into `output_path` (or back to `input_path` if not specified).
        """
        in_dir = Path(input_path)
        if output_path:
            out_dir = Path(output_path)
        else:
            out_dir = in_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) canonical entities → JSON
        for pkl in in_dir.glob("*_canonical_entities.pkl"):
            data = pickle.load(pkl.open("rb"))
            json_file = out_dir / f"{pkl.stem}.json"
            with json_file.open("w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Unpacked {pkl.name} → {json_file.name}")

        # 2) schema → JSON
        for pkl in in_dir.glob("*_schema.pkl"):
            data = pickle.load(pkl.open("rb"))
            json_file = out_dir / f"{pkl.stem}.json"
            with json_file.open("w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Unpacked {pkl.name} → {json_file.name}")

        # 3) processed data → CSV
        for pkl in in_dir.glob("*_processed_data.pkl"):
            obj = pd.read_pickle(pkl)
            if isinstance(obj, dict) and "tables" in obj:
                # combined mode: one CSV per table
                for tbl, df in obj["tables"].items():
                    csv_file = out_dir / f"{tbl}.csv"
                    df.to_csv(csv_file, index=False)
                    logger.info(f"Unpacked {pkl.name}[{tbl}] → {csv_file.name}")
            elif isinstance(obj, pd.DataFrame):
                csv_file = out_dir / f"{pkl.stem}.csv"
                obj.to_csv(csv_file, index=False)
                logger.info(f"Unpacked {pkl.name} → {csv_file.name}")
            else:
                # fallback: write JSON for anything else
                json_file = out_dir / f"{pkl.stem}.json"
                with json_file.open("w") as f:
                    json.dump(obj, f, indent=2)
                logger.info(f"Unpacked {pkl.name} → {json_file.name}")