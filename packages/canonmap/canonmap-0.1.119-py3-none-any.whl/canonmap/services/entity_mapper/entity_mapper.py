# canonmap/services/entity_mapper/entity_mapper.py

from pathlib import Path
import pickle
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from rapidfuzz import fuzz
from metaphone import doublemetaphone
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors

from canonmap.classes.embedder import Embedder
from canonmap.models.entity_mapping_request import EntityMappingRequest, TableFieldFilter
from canonmap.utils.logger import get_logger
from canonmap.utils.find_artifact_files import find_artifact_files
from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.services.entity_mapper.get_match_weights import get_match_weights

logger = get_logger("entity_mapper")


class EntityMapper:
    """
    Self-contained semantic + fuzzy + phonetic + initial + keyword matcher,
    applying user weights and filters, returning exactly num_results per query.
    """
    def __init__(self):
        # offline-only SBERT
        self.embedder = Embedder()

    def map_entities(self, config: EntityMappingRequest) -> List[Dict[str, Any]]:
        logger.info("Mapping entities: %r", config.entities)

        # 1) locate artifacts
        paths = find_artifact_files(config.artifacts_path)
        logger.debug("Artifacts found: %r", paths)

        # 2) load canonical entities
        ents: List[Dict[str, Any]] = pickle.loads(Path(paths["canonical_entities"]).read_bytes())
        N = len(ents)
        logger.info("Loaded %d canonical entities", N)

        # 3) load flat embeddings array
        arr = np.load(paths["canonical_entity_embeddings"])["embeddings"]
        if arr.shape[0] != N:
            raise ValueError(f"Entity/embedding length mismatch: {N} vs {arr.shape[0]}")

        # 4) prepare & normalize weights (copied from EntityMatcher)
        weights = get_match_weights(config.weights, config.use_semantic_search)

        # 5) precompute lookup arrays
        canon_strings = [m["_canonical_entity_"] for m in ents]
        phonetics = [doublemetaphone(s)[0] for s in canon_strings]

        # 6) optionally build semantic index
        nn: Optional[NearestNeighbors] = None
        embeddings = None
        if config.use_semantic_search:
            embeddings = normalize(arr.astype(np.float32), axis=1)
            k = min(50, N)
            nn = NearestNeighbors(n_neighbors=k, metric="cosine", n_jobs=get_cpu_count())
            nn.fit(embeddings)
            logger.info("Built semantic KNN (k=%d) on %d vectors", k, N)

        # 7) flatten field filters
        if config.filters:
            field_filter = []
            for filt in config.filters:
                table_fields = (filt.table_fields if isinstance(filt, TableFieldFilter)
                                else filt["table_fields"])
                field_filter.extend(table_fields)
            logger.debug("Applying field_filter: %r", field_filter)
        else:
            field_filter = None

        # 8–11) query loop
        results: List[Dict[str, Any]] = []
        pool = ThreadPoolExecutor(max_workers=self.embedder.num_workers)

        for query in config.entities:
            q = query.strip().lower()
            logger.debug("→ querying %r", q)

            # hybrid prune: semantic top-K + fuzzy top-M
            if nn:
                # embed query
                q_emb = self.embedder.embed_texts([query])[0].astype(np.float32)
                q_emb /= (np.linalg.norm(q_emb) + 1e-12)

                # top-K semantic candidates
                _, sem_nbrs = nn.kneighbors(q_emb.reshape(1, -1), return_distance=True)
                semantic_idxs = list(sem_nbrs[0])
                semantic_scores = (embeddings[semantic_idxs] @ q_emb) * 100

                # top-M fuzzy candidates across the entire corpus
                all_fuzzy = [
                    (i, fuzz.token_set_ratio(q, canon_strings[i].lower()))
                    for i in range(N)
                ]
                # take top 50 fuzzy by score
                top_fuzzy = sorted(all_fuzzy, key=lambda x: -x[1])[:50]
                fuzzy_idxs = [i for i, _ in top_fuzzy]

                # union the two sets
                cand_idxs = list(set(semantic_idxs) | set(fuzzy_idxs))
                # recompute semantic scores for any new fuzzy-only idxs
                sem_scores = [
                    (embeddings[i] @ q_emb) * 100 if embeddings is not None else 0.0
                    for i in cand_idxs
                ]
            else:
                cand_idxs = list(range(N))
                sem_scores = [0.0] * len(cand_idxs)

            # field filter
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

            # score all candidates in parallel
            futures = []

            def _score(i, sem_val):
                ent_str = canon_strings[i]
                sc = {
                    "semantic": sem_val,
                    "fuzzy": fuzz.token_set_ratio(q, ent_str.lower()),
                    "phonetic": 100 if doublemetaphone(q)[0] == phonetics[i] else 0,
                    "initial": 100
                        if "".join(w[0] for w in q.split())
                           == "".join(w[0] for w in ent_str.lower().split())
                        else 0,
                    "keyword": 100 if q == ent_str.lower().strip() else 0,
                }
                # weighted sum
                total = sum(sc[k] * weights[k] for k in sc)
                # cross‐metric bonuses/penalties
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

                return {
                    "entity": ent_str,
                    "score": float(total),
                    "passes": passes,
                    "metadata": ents[i],
                }

            for pos, i in enumerate(cand_idxs):
                sem_val = sem_scores[pos] if pos < len(sem_scores) else 0.0
                futures.append(pool.submit(_score, i, sem_val))

            scored = [f.result() for f in futures]

            # pick top‐K, prefer those that “pass” at least one metric
            passed = [r for r in scored if r["passes"] > 0] or scored
            passed.sort(key=lambda r: (-r["passes"], -r["score"]))
            results.append({
                "query": query,
                "matches": passed[: config.num_results]
            })

        pool.shutdown()
        return results