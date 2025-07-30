# canonmap/models/responses/entity_mapping_response.py
# Response model for entity mapping operations

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

    class Config:
        extra = "forbid"


class SingleMapping(BaseModel):
    """
    All of the matches for one input query.
    """
    query: str = Field(..., description="The original user query string")
    matches: List[MatchItem] = Field(
        ...,
        description="The ordered list of match items for this query"
    )

    @property
    def entities_list(self) -> List[str]:
        """
        List of just the entity strings in order of match ranking.
        """
        return [m.entity for m in self.matches]

    class Config:
        extra = "forbid"


class EntityMappingResponse(BaseModel):
    """
    The response for a bulk entity-mapping request.
    """
    results: List[SingleMapping] = Field(
        ...,
        description="One SingleMapping object per query"
    )

    def entities_to_dict(self) -> Dict[str, List[str]]:
        """
        Returns a dict mapping each query string to its list of matched entities.
        """
        return {sm.query: sm.entities_list for sm in self.results}

    class Config:
        extra = "forbid"