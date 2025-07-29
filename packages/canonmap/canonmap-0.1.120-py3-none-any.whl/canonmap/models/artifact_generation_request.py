# canonmap/models/artifact_generation_request.py

from typing import Optional, List, Dict, Union, Literal, Any
from pydantic import BaseModel, Field
import pandas as pd

DatabaseType = Literal["duckdb", "sqlite", "bigquery", "mariadb", "mysql", "postgresql"]

class EntityField(BaseModel):
    table_name: str
    field_name: str

class ArtifactGenerationRequest(BaseModel):
    input_path: Union[str, pd.DataFrame, Dict[str, Any]] = Field(
        ...,
        description="Path to CSV/JSON file or directory containing data files, "
                    "pandas DataFrame, or dict convertible to DataFrame."
    )
    output_path: Optional[str] = Field(
        None,
        description="Optional output directory path for generated artifacts."
    )
    source_name: str = Field(
        "data",
        description="Logical source name of the dataset."
    )
    table_name: Optional[str] = Field(
        None,
        description=(
            "Logical table name within the dataset. "
            "If not provided for a single-file input, "
            "it will be derived from the input file name."
        )
    )

    normalize_table_names: bool = Field(
        True,
        description="Normalize the table name to snake_case."
    )

    # Directory processing options
    recursive: bool = Field(
        False,
        description="If input_path is a directory, process files recursively."
    )
    file_pattern: str = Field(
        "*.csv",
        description="Pattern to match files when input_path is a directory (e.g. '*.csv', '*.json')."
    )
    table_name_from_file: bool = Field(
        True,
        description="When processing a directory, use the filename (without extension) as the table name."
    )

    entity_fields: Optional[List[EntityField]] = Field(
        None,
        description="List of entity fields with table and field names for canonicalization."
    )
    semantic_fields: Optional[List[str]] = Field(
        None,
        description="Column names used for semantic embeddings."
    )
    use_other_fields_as_metadata: bool = Field(
        False,
        description="Include non-entity fields as metadata for each canonical entity."
    )
    num_rows: Optional[int] = Field(
        None,
        description="Limit the number of rows to process."
    )

    generate_canonical_entities: bool = Field(
        True,
        description="Toggle whether to generate canonical entity list."
    )
    generate_schema: bool = Field(
        False,
        description="Toggle whether to infer a database schema."
    )
    generate_embeddings: bool = Field(
        False,
        description="Toggle whether to generate semantic embeddings for entities."
    )
    save_processed_data: bool = Field(
        False,
        description="Toggle whether to save a cleaned version of the input data."
    )

    schema_database_type: DatabaseType = Field(
        "duckdb",
        description="Target database dialect for schema generation."
    )
    clean_field_names: bool = Field(
        True,
        description="Clean column names to snake_case and remove special characters."
    )
    verbose: bool = Field(
        False,
        description="Enable verbose logging for debugging."
    )

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"