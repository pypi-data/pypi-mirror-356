# File: api/routes/mapping.py

from fastapi import APIRouter, Depends, HTTPException
from canonmap import CanonMap, EntityMappingRequest, EntityMappingResponse
from api.utils.get_canonmap import get_canonmap

router = APIRouter(tags=["mapping"])


@router.post(
    "/map-entities/",
    response_model=EntityMappingResponse,
    summary="Match user-supplied entities to canonical entities"
)
async def map_entities(
    request: EntityMappingRequest,
    canonmap: CanonMap = Depends(get_canonmap)
):
    """
    Map one or more entities to their canonical forms.
    """
    try:
        config = EntityMappingRequest(
            entities=request.entities,
            artifacts_path=request.artifacts_path,
            filters=request.filters,
            use_semantic_search=request.use_semantic_search,
            num_results=request.num_results,
            weights=request.weights,
            threshold=request.threshold,
            verbose=request.verbose
        )
        results = canonmap.map_entities(config=config)
        results_entities_dict = results.entities_to_dict()
        for query, entities in results_entities_dict.items():
            print(f"\nQuery: {query}")
            print(f"Entities: {entities}\n")
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))