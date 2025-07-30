# canonmap/models/artifact_generation_response.py

from typing import Any, Dict
from pydantic import BaseModel, Field

class ArtifactGenerationResponse(BaseModel):
    message: str = Field(
        ...,
        description="Summary of the artifact generation operation."
    )
    paths: Dict[str, Dict[str, str]] = Field(
        ...,
        description="Mapping from table (or source) name to a dict of artifact-name → path strings."
    )
    statistics: Dict[str, Any] = Field(
        ...,
        description=(
            "Operation metrics (e.g. total_tables, total_entities, "
            "total_embeddings, tables_processed)."
        )
    )

    class Config:
        extra = "forbid"