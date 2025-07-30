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
        self.base_artifacts_path = base_artifacts_path

    @lru_cache()
    def artifact_files(self, path: Optional[str] = None) -> dict:
        """
        Look up the schema/.pkl/.npz files under the given path.
        If no `path` is passed, falls back to the container’s base_artifacts_path.
        """
        target = path or self.base_artifacts_path
        if target is None:
            raise ValueError("No artifacts path provided for locating artifact files.")
        return find_artifact_files(target)

    @lru_cache()
    def embedder(self):
        return Embedder()

    @lru_cache()
    def nlp(self):
        return load_spacy_model()

    @lru_cache()
    def canonical_entities(self):
        files = self.artifact_files()
        with open(files["canonical_entities"], "rb") as f:
            return pickle.load(f)

    @lru_cache()
    def embeddings(self):
        files = self.artifact_files()
        arr = np.load(files["canonical_entity_embeddings"])[
            "embeddings"
        ]
        return normalize(arr.astype("float32"), axis=1)

    @lru_cache()
    def nn_index(self):
        ents = self.canonical_entities()
        k = min(50, len(ents))
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

        # Pass the finder function itself, not its result
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