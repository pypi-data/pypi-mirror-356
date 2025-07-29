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
from canonmap.utils.logger import get_logger

logger = get_logger("artifact_generator")


class ArtifactGenerator:
    def __init__(self) -> None:
        self.embedder = Embedder()
        self.nlp = load_spacy_model()

    def generate_artifacts(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        result = run_artifact_generation_pipeline(config, self.embedder, self.nlp)
        return result
