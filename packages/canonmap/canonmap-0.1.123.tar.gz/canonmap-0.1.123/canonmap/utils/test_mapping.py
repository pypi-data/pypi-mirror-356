# canonmap/utils/test_match.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

def test_mapping(
    idx: int,
    canonical_entities: List[Dict[str, Any]],
    canonical_entity_embeddings: np.ndarray,
    embedder
) -> Dict[str, Any]:
    """
    Given an index into your canonical_entities list and the flat embeddings array,
    re-embed the corresponding text and find its nearest neighbor in the stored matrix.

    Returns a dict with:
      - index_test: the input idx
      - original_text: text at that index
      - best_idx: index of the closest match
      - best_score: cosine similarity score of that match
      - recovered_text: text recovered at best_idx
      - match: bool, whether best_idx == idx
    """
    n = len(canonical_entities)
    if idx < 0 or idx >= n:
        raise IndexError(f"Index {idx} out of range (0–{n-1})")

    # 1) pull out the original text
    entity_meta = canonical_entities[idx]
    text = entity_meta["_canonical_entity_"]

    # 2) re-embed that text
    query_emb = embedder.embed_texts([text]).reshape(1, -1)

    # 3) compute cosine similarities against the stored embeddings
    sims = cosine_similarity(query_emb, canonical_entity_embeddings).flatten()

    # 4) find the best match
    best_idx = int(np.argmax(sims))
    best_score = float(sims[best_idx])
    recovered_meta = canonical_entities[best_idx]["_canonical_entity_"]

    return {
        "index_test": idx,
        "original_text": text,
        "best_idx": best_idx,
        "best_score": best_score,
        "recovered_text": recovered_meta,
        "match": best_idx == idx
    }