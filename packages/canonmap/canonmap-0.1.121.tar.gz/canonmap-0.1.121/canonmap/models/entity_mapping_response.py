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

class SingleMapping(BaseModel):
    """
    All of the matches for one input query.
    """
    query: str = Field(..., description="The original user query string")
    matches: List[MatchItem] = Field(
        ...,
        description="The ordered list of match items for this query"
    )

class EntityMappingResponse(BaseModel):
    """
    The response for a bulk entity-mapping request.
    """
    results: List[SingleMapping] = Field(
        ...,
        description="One SingleMapping object per query"
    )