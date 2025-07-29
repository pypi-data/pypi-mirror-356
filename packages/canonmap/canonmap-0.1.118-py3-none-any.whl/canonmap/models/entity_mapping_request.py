from typing import List
from pydantic import BaseModel, Field

class EntityMappingRequest(BaseModel):
    entities: List[str] = Field(
        ...,
        description="List of entities to map."
    )
    verbose: bool = Field(
        False,
        description="Enable verbose logging for debugging."
    )