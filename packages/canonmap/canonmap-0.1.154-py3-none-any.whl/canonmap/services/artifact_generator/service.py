# canonmap/services/artifact_generator/service.py

from canonmap import ArtifactGenerationRequest
from canonmap.embedder import Embedder
from canonmap.services.artifact_generator.pipeline import run_artifact_generation_pipeline
from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.utils.logger import get_logger

logger = get_logger("artifact_generator")

class ArtifactGenerator:
    def __init__(self, embedder=None, nlp=None):
        self.embedder = embedder or Embedder()
        self.nlp       = nlp       or load_spacy_model()

    def generate_artifacts(self, config: ArtifactGenerationRequest):
        return run_artifact_generation_pipeline(config, self.embedder, self.nlp)