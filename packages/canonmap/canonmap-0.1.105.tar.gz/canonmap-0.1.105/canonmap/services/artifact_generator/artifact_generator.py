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
        # embedder: Optional[Embedder] = None,
        # nlp: Optional[Any] = None,
    ) -> None:
        self.num_cores = get_cpu_count()
        self.embedder = Embedder(
            model_name="all-MiniLM-L6-v2",
            batch_size=1024,
            num_workers=self.num_cores
        )
        self.nlp = load_spacy_model()

        logger.info(f"Using device: {self.embedder.device}")
        logger.info(f"Detected {self.num_cores} CPU cores for parallel processing.")


    def generate_artifacts(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        result = run_artifact_generation_pipeline(config, self.embedder, self.nlp)
        return result
