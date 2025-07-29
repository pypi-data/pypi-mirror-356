from fastapi import APIRouter
from canonmap import CanonMap, EntityMappingRequest

router = APIRouter(tags=["mapping"])

@router.post("/map-entities/")
async def map_entities(request: EntityMappingRequest):
    """
    Map entities to canonical entities.
    """
    config = EntityMappingRequest(
        entities=request.entities,
        artifacts_path=request.artifacts_path,
        filters=request.filters,
        num_results=request.num_results,
        weights=request.weights,
        use_semantic_search=request.use_semantic_search,
        threshold=request.threshold,
        verbose=request.verbose
    )
    canonmap = CanonMap()
    result = canonmap.map_entities(config=config)
    return result