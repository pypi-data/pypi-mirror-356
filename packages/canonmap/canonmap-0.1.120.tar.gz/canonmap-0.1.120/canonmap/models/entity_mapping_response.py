# File: canonmap/models/entity_mapping_response.py

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class MatchItem(BaseModel):
    """
    A single match result for one query.
    """
    entity: str = Field(..., description="The matched canonical entity string")
    score: float = Field(..., description="The combined match score (0–100)")
    passes: int = Field(
        ...,
        description="Number of individual metrics that exceeded the configured threshold"
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Original metadata dictionary for this entity"
    )


class EntityMappingResponse(BaseModel):
    """
    The response for a bulk entity-mapping request.
    Each list item is a dict mapping the original query string
    to its list of MatchItem results.
    """
    results: List[Dict[str, List[MatchItem]]] = Field(
        ...,
        description=(
            "A list where each element is a single-key dict. "
            "The key is the original query string; the value is "
            "the ordered list of MatchItems for that query."
        )
    )