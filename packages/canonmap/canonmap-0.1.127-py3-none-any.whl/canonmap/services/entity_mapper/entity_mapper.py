# canonmap/services/entity_mapper/entity_mapper.py

from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from rapidfuzz import fuzz
from metaphone import doublemetaphone
from sklearn.neighbors import NearestNeighbors

from canonmap.models.entity_mapping_request import EntityMappingRequest, TableFieldFilter
from canonmap.models.entity_mapping_response import EntityMappingResponse, SingleMapping, MatchItem
from canonmap.services.entity_mapper.get_match_weights import get_match_weights
from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.utils.logger import get_logger

import numpy as np

logger = get_logger("entity_mapper")


class EntityMapper:
    """
    Hybrid semantic + fuzzy + phonetic + initial + keyword matcher,
    parallelized over the input list. All artifact loading and index
    building is done *outside* of this class.
    """
    def __init__(
        self,
        embedder,
        canonical_entities: List[Dict[str, Any]],
        embeddings: np.ndarray,
        nn: Optional[NearestNeighbors],
    ):
        self.embedder = embedder
        self.ents = canonical_entities
        self.embeddings = embeddings
        self.nn = nn
        self.N = len(canonical_entities)
        self.canon_strings = [e["_canonical_entity_"] for e in canonical_entities]
        self.phonetics = [doublemetaphone(s)[0] for s in self.canon_strings]

    def map_entities(self, config: EntityMappingRequest) -> EntityMappingResponse:
        weights = get_match_weights(config.weights, config.use_semantic_search)

        # flatten filters
        if config.filters:
            ff = []
            for filt in config.filters:
                fields = filt.table_fields if isinstance(filt, TableFieldFilter) else filt["table_fields"]
                ff.extend(fields)
            field_filter = set(ff)
        else:
            field_filter = None

        def _process_one(query: str) -> SingleMapping:
            q_norm = query.strip().lower()

            # 1) hybrid candidate union
            if self.nn and config.use_semantic_search:
                # embed + normalize
                q_emb = self.embedder.embed_texts([query])[0].astype(np.float32)
                q_emb /= (np.linalg.norm(q_emb) + 1e-12)

                # semantic neighbors
                _, nbrs = self.nn.kneighbors(q_emb.reshape(1, -1), return_distance=True)
                sem_idxs = list(nbrs[0])
                sem_scores = (self.embeddings[sem_idxs] @ q_emb) * 100

                # fuzzy top-50
                all_fz = [(i, fuzz.token_set_ratio(q_norm, self.canon_strings[i].lower()))
                          for i in range(self.N)]
                fuzzy_idxs = [i for i, _ in sorted(all_fz, key=lambda x: -x[1])[:50]]

                # union + recompute semantic scores for new idxs
                cand_idxs = list(set(sem_idxs) | set(fuzzy_idxs))
                sem_scores = [
                    (self.embeddings[i] @ q_emb) * 100 if i in sem_idxs else 0.0
                    for i in cand_idxs
                ]
            else:
                cand_idxs = list(range(self.N))
                sem_scores = [0.0] * len(cand_idxs)

            # 2) apply field filter
            if field_filter:
                filtered = [
                    (idx, sem_scores[pos])
                    for pos, idx in enumerate(cand_idxs)
                    if self.ents[idx].get("_field_name_") in field_filter
                ]
                cand_idxs, sem_scores = zip(*filtered) if filtered else ([], [])

            # 3) scoring
            scored: List[MatchItem] = []
            for pos, idx in enumerate(cand_idxs):
                base = self.canon_strings[idx]
                sc = {
                    "semantic": sem_scores[pos],
                    "fuzzy": fuzz.token_set_ratio(q_norm, base.lower()),
                    "phonetic": 100 if doublemetaphone(q_norm)[0] == self.phonetics[idx] else 0,
                    "initial": 100 if "".join(w[0] for w in q_norm.split())
                                  == "".join(w[0] for w in base.lower().split()) else 0,
                    "keyword": 100 if q_norm == base.lower().strip() else 0,
                }
                total = sum(sc[k] * weights[k] for k in sc)
                # bonuses/penalties (same as before)...
                if sc["semantic"] > 80 and sc["fuzzy"] > 80: total += 10
                if sc["fuzzy"] > 90 and sc["semantic"] < 60:  total -= 15
                if sc["initial"] == 100:                    total += 10
                if sc["phonetic"] == 100:                  total += 5
                total = min(total, 100.0)

                passes = sum(1 for v in sc.values() if v >= config.threshold)
                scored.append(MatchItem(
                    entity=base,
                    score=float(total),
                    passes=passes,
                    metadata=self.ents[idx]
                ))

            # 4) sort & take top-K
            final = [r for r in scored if r.passes > 0] or scored
            final.sort(key=lambda r: (-r.passes, -r.score))

            logger.info(f"Final: {final}")
            return SingleMapping(query=query, matches=final[:config.num_results])

        # 5) parallel execute
        max_workers = min(len(config.entities), get_cpu_count())
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(_process_one, config.entities))

        return EntityMappingResponse(results=results)