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
