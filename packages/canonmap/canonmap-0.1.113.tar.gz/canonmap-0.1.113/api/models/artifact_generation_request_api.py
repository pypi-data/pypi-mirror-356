# File: api/models/artifact_generation_request_api.py

from typing import List, Dict, Any, Optional, Union, Literal
from pydantic import BaseModel, Field

DatabaseType = Literal["duckdb", "sqlite", "bigquery", "mariadb", "mysql", "postgresql"]


class EntityFieldEntry(BaseModel):
    table_name: str = Field(..., description="Logical table name where the field is located.")
    field_name: str = Field(..., description="Name of the entity field to extract canonical values from.")


class ArtifactGenerationRequestAPI(BaseModel):
    """
    API-facing request model matching ArtifactGenerationRequest from canonmap.models.
    """

    input_path: Union[str, Dict[str, Any]] = Field(
        ..., description="CSV/JSON path or dict convertible to DataFrame. Can be a directory path for multi-table processing."
    )
    output_path: Optional[str] = Field(
        None, description="Optional output directory path for generated artifacts."
    )
    source_name: str = Field("data", description="Logical source name of the dataset.")
    table_name: str = Field("data", description="Logical table name within the dataset. For multi-table processing, this is used as a prefix.")

    entity_fields: Optional[List[EntityFieldEntry]] = Field(
        None, description="List of fields to treat as entities, each with table and field name."
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

    # New fields for multi-table processing
    recursive: bool = Field(
        False, description="Process directories recursively when input_path is a directory."
    )
    file_pattern: Optional[str] = Field(
        None, description="Glob pattern to match files when processing a directory (e.g., '*.csv')."
    )
    table_name_from_file: bool = Field(
        True, description="Use the file name (without extension) as the table name when processing multiple files."
    )

    class Config:
        extra = "forbid"