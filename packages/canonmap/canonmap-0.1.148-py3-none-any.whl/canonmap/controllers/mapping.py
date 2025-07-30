# canonmap/controllers/mapping.py

from canonmap.models.entity_mapping_request import EntityMappingRequest
from canonmap.services.entity_mapper import EntityMapper

class MappingController:
    """
    Controller for entity‐to‐canonical matching.
    """

    def __init__(
        self,
        embedder,
        canonical_entities: list,
        embeddings,            # numpy.ndarray
        nn,                    # sklearn NearestNeighbors or None
    ):
        self.mapper = EntityMapper(
            embedder=embedder,
            canonical_entities=canonical_entities,
            embeddings=embeddings,
            nn=nn,
        )

    def run(self, config: EntityMappingRequest):
        """
        Map each input entity string to its top K canonical matches.
        """
        return self.mapper.map_entities(config)