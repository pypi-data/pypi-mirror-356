# canonmap/controllers/generation.py

from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.services.artifact_generator import ArtifactGenerator

class GenerationController:
    """
    Controller for artifact generation.
    """

    def __init__(self, embedder, nlp):
        # embedder: an Embedder instance
        # nlp: a spaCy NLP pipeline
        self.generator = ArtifactGenerator(embedder=embedder, nlp=nlp)

    def run(self, config: ArtifactGenerationRequest):
        """
        Kick off the artifact generation pipeline and return its response model.
        """
        return self.generator.generate_artifacts(config)