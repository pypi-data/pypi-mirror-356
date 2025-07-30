# canonmap/models/entity_mapping_request.py

from pathlib import Path
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator

class TableFieldFilter(BaseModel):
    table_name: str = Field(
        ...,
        description="Name of the table to include in matching."
    )
    table_fields: List[str] = Field(
        ...,
        description="List of field names within that table to restrict to."
    )

class EntityMappingRequest(BaseModel):
    entities: List[str] = Field(
        ...,
        description="List of raw entity strings to map."
    )
    artifacts_path: Optional[Path] = Field(
        None,
        description="Directory where schema, entities, and embeddings live. "
                    "If omitted, uses the `CanonMap` instance’s path."
    )
    filters: List[TableFieldFilter] = Field(
        default_factory=list,
        description="Optional per-table filters to constrain matching fields."
    )
    num_results: int = Field(
        15,
        ge=1,
        description="Maximum number of matches to return."
    )
    weights: Dict[str, float] = Field(
        default_factory=lambda: {
            'semantic': 0.40,
            'fuzzy':    0.40,
            'initial':  0.10,
            'keyword':  0.05,
            'phonetic': 0.05,
        },
        description="Relative weights for each matching strategy (must sum to >0)."
    )
    use_semantic_search: bool = Field(
        True,
        description="Whether to include semantic-search–based matching."
    )
    threshold: float = Field(
        0.0,
        ge=0.0,
        le=100.0,
        description="Score threshold (0–100) for a metric to count as a ‘pass’.",
    )
    verbose: bool = Field(
        False,
        description="Enable verbose logging."
    )

    @validator("weights")
    def _check_weights_sum(cls, w: Dict[str, float]):
        total = sum(w.values())
        if total <= 0:
            raise ValueError("Sum of all weight values must be greater than 0")
        return w

    class Config:
        extra = "forbid"