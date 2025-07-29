import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from typing import List, Tuple, Union, Dict
import logging
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from canonmap.utils.get_cpu_count import get_cpu_count

logger = logging.getLogger(__name__)

class Embedder:
    """
    Embeds multiple named lists of texts in one go. Flattens all jobs,
    does a single model.encode call, and then splits the embeddings back out.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", batch_size: int = 256):
        self.device = self._resolve_device()
        logger.info(f"🔌 Using device: {self.device}")
        self._model = SentenceTransformer(model_name, device=self.device)
        self.batch_size = batch_size
        self.num_workers = get_cpu_count()

    def _resolve_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def embed_texts(
        self,
        texts_or_jobs: Union[List[str], List[Tuple[str, List[str]]]],
        tag: str = "embedding"
    ) -> Union[np.ndarray, Dict[str, np.ndarray]]:
        # single‐job fallback
        if isinstance(texts_or_jobs[0], str):
            return self._model.encode(
                texts_or_jobs,
                batch_size=self.batch_size,
                show_progress_bar=False,
                num_workers=self.num_workers
            )

        # multiple jobs: flatten them into one big list
        all_texts: List[str] = []
        boundaries: Dict[str, Tuple[int,int]] = {}
        for name, texts in texts_or_jobs:
            start = len(all_texts)
            all_texts.extend(texts)
            end = len(all_texts)
            boundaries[name] = (start, end)

        if not all_texts:
            return {name: np.empty((0, self._model.get_sentence_embedding_dimension()))
                    for name, _ in texts_or_jobs}

        logger.info(f"⚙️ Embedding {len(all_texts)} texts across {len(boundaries)} jobs…")
        embeddings = self._model.encode(
            all_texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            num_workers=self.num_workers
        )

        # slice back out per job
        result: Dict[str, np.ndarray] = {}
        for name, (start, end) in boundaries.items():
            result[name] = embeddings[start:end]

        return result