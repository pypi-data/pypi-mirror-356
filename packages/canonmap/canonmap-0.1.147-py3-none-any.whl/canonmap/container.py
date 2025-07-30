# canonmap/container.py

from functools import lru_cache
from typing import Optional

from canonmap.utils.find_artifact_files import find_artifact_files
from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.embedder import Embedder
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors
import pickle

class Container:
    def __init__(self, base_artifacts_path: Optional[str] = None):
        # May be None if user only calls .generate()
        self.base_artifacts_path = base_artifacts_path

    @lru_cache()
    def artifact_files(self):
        if self.base_artifacts_path is None:
            raise ValueError("No artifacts_path provided to Container")
        return find_artifact_files(self.base_artifacts_path)

    @lru_cache()
    def embedder(self):
        return Embedder()

    @lru_cache()
    def nlp(self):
        return load_spacy_model()

    @lru_cache()
    def canonical_entities(self):
        with open(self.artifact_files()["canonical_entities"], "rb") as f:
            return pickle.load(f)

    @lru_cache()
    def embeddings(self):
        arr = np.load(self.artifact_files()["canonical_entity_embeddings"])["embeddings"]
        return normalize(arr.astype("float32"), axis=1)

    @lru_cache()
    def nn_index(self):
        k = min(50, len(self.canonical_entities()))
        nn = NearestNeighbors(n_neighbors=k, metric="cosine")
        nn.fit(self.embeddings())
        return nn

    @lru_cache()
    def generation_controller(self):
        from canonmap.controllers.generation import GenerationController
        return GenerationController(
            embedder=self.embedder(),
            nlp=self.nlp(),
        )

    
    @lru_cache()
    def unpacking_controller(self):
        from canonmap.controllers.unpacking import UnpackingController
        return UnpackingController(
            unpack_finder=self.artifact_files,
        )


    @lru_cache()
    def mapping_controller(self):
        from canonmap.controllers.mapping import MappingController
        return MappingController(
            embedder=self.embedder(),
            canonical_entities=self.canonical_entities(),
            embeddings=self.embeddings(),
            nn=self.nn_index(),
        )