# File: canonmap/core.py

import logging
from typing import Optional, Dict, Any
from pathlib import Path

from pydantic import BaseModel, Field

from canonmap.classes.embedder import Embedder
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest

from canonmap.services.artifact_generator import ArtifactGenerator
from canonmap.services.artifact_unpacker import ArtifactUnpacker
from canonmap.services.entity_mapper.entity_mapper import EntityMapper

from canonmap.utils.find_artifact_files import find_artifact_files
from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.utils.logger import get_logger

import pickle
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors

logger = get_logger("core")


def toggle_logging(verbose: bool):
    if verbose:
        logging.disable(logging.NOTSET)
    else:
        logging.disable(logging.INFO)


class CanonMap:
    """
    Public API interface for canonmap.
    Handles generation of artifacts and matching entities using provided configuration objects.
    """
    def __init__(self, artifacts_path: str):
        # Remember once for both startup and request-time defaults
        self.artifacts_path = artifacts_path
        self.controller = CanonMapController(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        toggle_logging(config.verbose)
        return self.controller.run_pipeline(config)

    def unpack(self, config: ArtifactUnpackingRequest) -> Dict[str, Any]:
        toggle_logging(config.verbose)
        return self.controller.unpack_artifacts(config)

    def map_entities(self, config: EntityMappingRequest) -> Any:
        # Default to the controller's path if caller omitted it
        if not config.artifacts_path:
            config.artifacts_path = self.artifacts_path
        toggle_logging(config.verbose)
        logger.info(f"Mapping entities (using artifacts at '{config.artifacts_path}')")
        return self.controller.run_entity_mapping(config)


class CanonMapController:
    """
    Holds all the “load once” state (embedder, spaCy, artifact files,
    canonical entities, embeddings, and semantic index) so that
    per-request calls are fast.
    """
    def __init__(self, artifacts_path: str):
        # discover & cache artifact file paths
        self.artifact_files = find_artifact_files(artifacts_path)

        # shared embedder & spaCy
        self.embedder = Embedder()
        self.nlp = load_spacy_model()

        # load canonical entities
        with open(self.artifact_files["canonical_entities"], "rb") as f:
            self.canonical_entities = pickle.load(f)

        # load & normalize embeddings
        arr = np.load(self.artifact_files["canonical_entity_embeddings"])["embeddings"]
        if arr.shape[0] != len(self.canonical_entities):
            raise ValueError(
                f"Entity/embedding length mismatch: "
                f"{len(self.canonical_entities)} vs {arr.shape[0]}"
            )
        self.embeddings = normalize(arr.astype(np.float32), axis=1)

        # build semantic-search index
        k = min(50, len(self.canonical_entities))
        self.nn = NearestNeighbors(n_neighbors=k, metric="cosine")
        self.nn.fit(self.embeddings)
        logger.info(f"Built semantic KNN index with k={k}")

        # downstream services reuse all that state
        self.artifact_generator = ArtifactGenerator(
            embedder=self.embedder,
            nlp=self.nlp,
        )
        self.artifact_unpacker = ArtifactUnpacker(
            artifact_files=self.artifact_files
        )
        self.entity_mapper = EntityMapper(
            embedder=self.embedder,
            canonical_entities=self.canonical_entities,
            embeddings=self.embeddings,
            nn=self.nn,
            artifact_files=self.artifact_files,
        )

    def run_pipeline(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        return self.artifact_generator.generate_artifacts(config)

    def unpack_artifacts(self, config: ArtifactUnpackingRequest) -> Dict[str, Any]:
        return self.artifact_unpacker.unpack_artifacts(config)

    def run_entity_mapping(self, config: EntityMappingRequest) -> Any:
        return self.entity_mapper.map_entities(config)