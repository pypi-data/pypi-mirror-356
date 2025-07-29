# File: canonmap/services/entity_mapper/entity_mapper.py

from pathlib import Path
import pickle
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from rapidfuzz import fuzz
from metaphone import doublemetaphone
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors

from canonmap.classes.embedder import Embedder
from canonmap.models.entity_mapping_request import EntityMappingRequest, TableFieldFilter
from canonmap.models.entity_mapping_response import EntityMappingResponse, MatchItem
from canonmap.services.entity_mapper.get_match_weights import get_match_weights
from canonmap.utils.find_artifact_files import find_artifact_files
from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.utils.logger import get_logger

logger = get_logger("entity_mapper")


class EntityMapper:
    """
    Self-contained semantic + fuzzy + phonetic + initial + keyword matcher,
    now parallelized over the list of input entities.
    """
    def __init__(self):
        # SBERT or similar offline embedder
        self.embedder = Embedder()

    def map_entities(self, config: EntityMappingRequest) -> EntityMappingResponse:
        logger.info("Bulk mapping %d entities", len(config.entities))

        # 1) load artifacts
        paths = find_artifact_files(config.artifacts_path)
        ents: List[Dict[str, Any]] = pickle.loads(Path(paths["canonical_entities"]).read_bytes())
        N = len(ents)
        logger.info("Loaded %d canonical entities", N)

        # 2) load embeddings
        arr = np.load(paths["canonical_entity_embeddings"])["embeddings"]
        if arr.shape[0] != N:
            raise ValueError(f"Entity/embedding length mismatch: {N} vs {arr.shape[0]}")

        # 3) weights
        weights = get_match_weights(config.weights, config.use_semantic_search)

        # 4) prepare lookup tables
        canon_strings = [m["_canonical_entity_"] for m in ents]
        phonetics = [doublemetaphone(s)[0] for s in canon_strings]

        # 5) semantic index
        nn: Optional[NearestNeighbors] = None
        embeddings: Optional[np.ndarray] = None
        if config.use_semantic_search:
            embeddings = normalize(arr.astype(np.float32), axis=1)
            k = min(50, N)
            nn = NearestNeighbors(n_neighbors=k, metric="cosine", n_jobs=get_cpu_count())
            nn.fit(embeddings)
            logger.info("Built semantic KNN (k=%d)", k)

        # 6) flatten filters
        field_filter: Optional[List[str]]
        if config.filters:
            ff: List[str] = []
            for filt in config.filters:
                fields = filt.table_fields if isinstance(filt, TableFieldFilter) else filt["table_fields"]
                ff.extend(fields)
            field_filter = ff
            logger.debug("Will restrict to fields: %r", field_filter)
        else:
            field_filter = None

        # 7) define single-query logic
        def _process_one(query: str) -> Dict[str, List[MatchItem]]:
            q_norm = query.strip().lower()

            # semantic + fuzzy candidate union
            if nn:
                # embed + normalize
                q_emb = self.embedder.embed_texts([query])[0].astype(np.float32)
                q_emb /= (np.linalg.norm(q_emb) + 1e-12)

                # top-K semantic
                _, nbrs = nn.kneighbors(q_emb.reshape(1, -1), return_distance=True)
                sem_idxs = list(nbrs[0])
                sem_scores = (embeddings[sem_idxs] @ q_emb) * 100

                # top-M fuzzy
                all_fuzzy = [(i, fuzz.token_set_ratio(q_norm, canon_strings[i].lower()))
                             for i in range(N)]
                top_fuzzy = sorted(all_fuzzy, key=lambda x: -x[1])[:50]
                fuzzy_idxs = [i for i, _ in top_fuzzy]

                # union
                cand_idxs = list(set(sem_idxs) | set(fuzzy_idxs))
                # recompute any missing semantic scores
                sem_scores = [
                    (embeddings[i] @ q_emb) * 100 if i in sem_idxs else 0.0
                    for i in cand_idxs
                ]
            else:
                cand_idxs = list(range(N))
                sem_scores = [0.0] * N

            # apply field filter
            if field_filter:
                filtered = [
                    (idx, sem_scores[pos])
                    for pos, idx in enumerate(cand_idxs)
                    if ents[idx].get("_field_name_") in field_filter
                ]
                if filtered:
                    cand_idxs, sem_scores = zip(*filtered)
                    cand_idxs, sem_scores = list(cand_idxs), list(sem_scores)
                else:
                    cand_idxs, sem_scores = [], []

            # now score each candidate
            scored: List[MatchItem] = []
            for pos, idx in enumerate(cand_idxs):
                base = canon_strings[idx]
                sc_sem = sem_scores[pos] if pos < len(sem_scores) else 0.0
                sc = {
                    "semantic": sc_sem,
                    "fuzzy": fuzz.token_set_ratio(q_norm, base.lower()),
                    "phonetic": 100 if doublemetaphone(q_norm)[0] == phonetics[idx] else 0,
                    "initial": 100
                        if "".join(w[0] for w in q_norm.split())
                           == "".join(w[0] for w in base.lower().split())
                        else 0,
                    "keyword": 100 if q_norm == base.lower().strip() else 0,
                }
                # weighted sum
                total = sum(sc[m] * weights[m] for m in sc)
                # bonuses/penalties
                if sc["semantic"] > 80 and sc["fuzzy"] > 80:
                    total += 10
                if sc["fuzzy"] > 90 and sc["semantic"] < 60:
                    total -= 15
                if sc["initial"] == 100:
                    total += 10
                if sc["phonetic"] == 100:
                    total += 5
                total = min(total, 100.0)

                passes = sum(1 for v in sc.values() if v >= config.threshold)

                scored.append(MatchItem(
                    entity=base,
                    score=total,
                    passes=passes,
                    metadata=ents[idx]
                ))

            # sort & take top-N
            passed = [r for r in scored if r.passes > 0] or scored
            passed.sort(key=lambda r: (-r.passes, -r.score))
            return {query: passed[: config.num_results]}

        # 8) parallelize across queries
        max_workers = min(len(config.entities), get_cpu_count())
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            items = list(executor.map(_process_one, config.entities))

        return EntityMappingResponse(results=items)