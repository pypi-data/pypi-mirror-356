# File: canonmap/services/artifact_generator/artifact_generator.py

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
from canonmap.utils.logger import get_logger

logger = get_logger("artifact_generator")


class ArtifactGenerator:
    """
    Generates artifacts (schema, entities, embeddings, etc.) from input data.
    Now accepts a pre-loaded artifact_files dict if provided.
    """
    def __init__(
        self,
        embedder: Optional[Embedder] = None,
        nlp: Optional[Any] = None,
    ) -> None:
        self.embedder = embedder or Embedder()
        self.nlp = nlp or load_spacy_model()

    def generate_artifacts(
        self,
        config: ArtifactGenerationRequest
    ) -> Dict[str, Any]:
        """
        Run the pipeline, passing along the embedder, nlp, and any preloaded artifact_files.
        """
        result = run_artifact_generation_pipeline(
            config,
            embedder=self.embedder,
            nlp=self.nlp,
        )
        return result