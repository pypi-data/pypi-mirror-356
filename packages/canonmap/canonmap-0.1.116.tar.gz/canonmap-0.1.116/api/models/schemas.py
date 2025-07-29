# File: api/models/schemas.py

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
# from canonmap.models.artifact_request import ArtifactGenerationRequest as GenerateRequest
# from canonmap.models.artifact_response import ArtifactGenerationResponse as GenerateResponse


from typing import Optional, List, Union, Dict, Any, Literal
from pydantic import BaseModel, Field

DatabaseType = Literal["duckdb", "sqlite", "bigquery", "mariadb", "mysql", "postgresql"]

class ArtifactGenerationRequestAPI(BaseModel):
    """
    API-facing request model matching ArtifactGenerationRequest from canonmap.models.
    """

    input_path: Union[str, Dict[str, Any]] = Field(
        ..., description="CSV/JSON path or dict convertible to DataFrame."
    )
    output_path: Optional[str] = Field(
        None, description="Optional output directory path for generated artifacts."
    )
    source_name: str = Field("data", description="Logical source name of the dataset.")
    table_name: str = Field("data", description="Logical table name within the dataset.")

    entity_fields: Optional[List[str]] = Field(
        None, description="Column names to treat as entity fields for canonicalization."
    )
    semantic_fields: Optional[List[str]] = Field(
        None, description="Column names used for semantic embeddings."
    )
    use_other_fields_as_metadata: bool = Field(
        False, description="Include non-entity fields as metadata for each canonical entity."
    )
    num_rows: Optional[int] = Field(
        None, description="Limit the number of rows to process."
    )

    generate_canonical_entities: bool = Field(
        True, description="Toggle whether to generate canonical entity list."
    )
    generate_schema: bool = Field(
        False, description="Toggle whether to infer a database schema."
    )
    generate_embeddings: bool = Field(
        False, description="Toggle whether to generate semantic embeddings for entities."
    )
    save_processed_data: bool = Field(
        False, description="Toggle whether to save a cleaned version of the input data."
    )

    schema_database_type: DatabaseType = Field(
        "duckdb", description="Target database dialect for schema generation."
    )
    clean_field_names: bool = Field(
        False, description="Clean column names to snake_case and remove special characters."
    )
    verbose: bool = Field(
        False, description="Enable verbose logging for debugging."
    )


# class GenerateResponse(BaseModel):
#     """Response model for artifact generation."""
#     message: str = Field(..., description="Confirmation message for generation status.")
#     paths: Dict[str, str] = Field(..., description="Paths to generated artifacts (pickles, npz, etc.).")


class MatchRequest(BaseModel):
    """Request model for entity matching."""
    entity_term: str = Field(..., description="The entity term to match")
    canonical_entities_path: str = Field(..., description="Path to the canonical_entities.pkl file")
    canonical_entity_embeddings_path: Optional[str] = Field(None, description="Path to the canonical_entity_embeddings.npz file (required if use_semantic_search=True)")
    schema_path: Optional[str] = Field(None, description="Path to the schema.pkl file (not used in matching)")
    top_k: int = Field(5, description="Maximum number of results to return")
    threshold: float = Field(0, description="Minimum score threshold for matches")
    field_filter: Optional[List[str]] = Field(None, description="List of field names to restrict matching to")
    use_semantic_search: bool = Field(False, description="Whether to enable semantic search")
    weights: Optional[Dict[str, float]] = Field(None, description="Custom weights for different matching strategies")
    verbose: bool = Field(False, description="Whether to show detailed logging")

class MatchResult(BaseModel):
    """Response model for a single match result."""
    entity: str = Field(..., description="The matched entity string")
    score: float = Field(..., description="Match score (0-100)")
    passes: int = Field(..., description="Number of individual matching strategies that passed")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata for the matched entity")

class MatchResponse(BaseModel):
    """Response model for entity matching."""
    results: List[MatchResult] = Field(..., description="List of match results")
