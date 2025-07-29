# canonmap/models/entity_mapping_request.py

from typing import List, Optional, Dict
from pydantic import BaseModel, Field

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
        description="List of entities to map."
    )
    artifacts_path: str = Field(
        ...,
        description="Path to the artifacts directory (schema, entities, embeddings)."
    )
    filters: Optional[List[TableFieldFilter]] = Field(
        default_factory=list,
        description=(
            "Optional list of per-table filters. "
            "Each filter restricts matching to only those fields in that table."
        )
    )
    num_results: int = Field(
        default=15,
        description="Number of results to return."
    )
    weights: Dict[str, float] = Field(
        default_factory=lambda: {
            'semantic': 0.40,
            'fuzzy':    0.40,
            'initial':  0.10,
            'keyword':  0.05,
            'phonetic': 0.05,
        },
        description="Relative weights to apply for each matching strategy."
    )
    use_semantic_search: bool = Field(
        default=True,
        description="Whether to include semantic-search–based matching."
    )
    threshold: float = Field(
        default=0.0,
        description="Score threshold (0–100) that a given metric must exceed to count as a ‘pass’."
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose logging for debugging."
    )