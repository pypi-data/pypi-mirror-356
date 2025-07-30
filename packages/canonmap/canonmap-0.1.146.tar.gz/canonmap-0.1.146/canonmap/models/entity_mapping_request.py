# canonmap/models/entity_mapping_request.py

from pathlib import Path
from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, validator, ConfigDict

class TableFieldFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str = Field(
        ...,
        description="Name of the table to include in matching."
    )
    table_fields: List[str] = Field(
        ...,
        description="Fields within that table to match."
    )

class EntityMappingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entities: List[str] = Field(
        ...,
        description="List of raw entity strings to map."
    )
    artifacts_path: Optional[Union[str, Path]] = Field(
        None,
        description="Directory where artifacts live; defaults to the CanonMap instance’s path."
    )
    filters: List[TableFieldFilter] = Field(
        default_factory=list,
        description="Optional per-table filters to restrict matching fields."
    )
    num_results: int = Field(
        15,
        ge=1,
        description="Max number of matches per query."
    )
    weights: Dict[str, float] = Field(
        default_factory=lambda: {
            'semantic': 0.40,
            'fuzzy':    0.40,
            'initial':  0.10,
            'keyword':  0.05,
            'phonetic': 0.05,
        },
        description="Relative weights for each matching strategy (sum > 0)."
    )
    use_semantic_search: bool = Field(
        True,
        description="Whether to include semantic-search–based matching."
    )
    threshold: float = Field(
        0.0,
        ge=0.0,
        le=100.0,
        description="Score threshold (0–100) for a metric to count as a ‘pass’."
    )
    verbose: Optional[bool] = Field(
        None,
        description="If set, overrides the CanonMap default_verbose; otherwise inherits it."
    )

    @validator("weights")
    def _check_weights_sum(cls, w: Dict[str, float]):
        total = sum(w.values())
        if total <= 0:
            raise ValueError("Sum of weight values must be greater than 0")
        return w