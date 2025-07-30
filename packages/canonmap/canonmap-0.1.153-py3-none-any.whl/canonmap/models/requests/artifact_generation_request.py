# canonmap/models/requests/artifact_generation_request.py
# Request model for artifact generation operations

from __future__ import annotations
from pathlib import Path
from typing import Optional, List, Dict, Union, Literal, Any
from pydantic import BaseModel, Field, root_validator, ConfigDict
import pandas as pd

DatabaseType = Literal["duckdb", "sqlite", "bigquery", "mariadb", "mysql", "postgresql"]

class EntityField(BaseModel):
    """Configuration for a field to be canonicalized.
    
    Args:
        table_name: Name of the table containing the entity field
        field_name: Name of the field to canonicalize
    """
    table_name: str = Field(..., description="Name of the table containing the entity field.")
    field_name: str = Field(..., description="Name of the field to canonicalize.")

class ArtifactGenerationRequest(BaseModel):
    """Configuration for generating canonicalization artifacts.
    
    This model defines all parameters needed to generate canonicalization artifacts
    from input data. It supports various input formats and configuration options
    for controlling the artifact generation process.

    Args:
        input_path: Path (file/directory) or DataFrame or dict to process
        output_path: Directory for generated artifacts (default: input file's parent)
        source_name: Logical name for the data source (default: "data")
        table_name: Logical table name (default: derived from filename)
        normalize_table_names: Whether to normalize table names to snake_case (default: True)
        recursive: Whether to recurse into subdirectories (default: False)
        file_pattern: Glob pattern for selecting files (default: "*.csv")
        table_name_from_file: Use filename as table name for multiple files (default: True)
        entity_fields: List of specific table/field pairs to canonicalize (default: None)
        semantic_fields: Column names for semantic embeddings (default: None)
        use_other_fields_as_metadata: Treat non-entity columns as metadata (default: False)
        num_rows: Maximum rows to process per source (default: None)
        generate_canonical_entities: Whether to build canonical entity list (default: True)
        generate_schema: Whether to infer and emit database schema (default: False)
        generate_embeddings: Whether to compute entity embeddings (default: False)
        save_processed_data: Whether to save cleaned input data (default: False)
        schema_database_type: Target SQL dialect for schema (default: "duckdb")
        clean_field_names: Whether to clean column names (default: True)
        verbose: Override CanonMap's verbosity setting (default: None)
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "input_path": "data/input.csv",
                    "source_name": "customer_data",
                    "entity_fields": [{"table_name": "customers", "field_name": "name"}],
                    "generate_schema": True,
                    "schema_database_type": "mariadb"
                }
            ]
        }
    )

    # allow both strings and Paths, plus DataFrame or dict
    input_path: Union[str, Path, pd.DataFrame, Dict[str, Any]] = Field(
        ...,
        description=(
            "Path (file or directory) or pandas DataFrame, or a dict convertible to one."
        )
    )

    # accept str or Path, optional
    output_path: Optional[Union[str, Path]] = Field(
        None,
        description=(
            "Directory where generated artifacts will be written. "
            "If unset and `input_path` is a single file, defaults to its parent directory."
        )
    )

    # all of these have defaults, so IDE knows you don't have to pass them
    source_name: str = Field("data", description="Logical name for the data source.")
    table_name: Optional[str] = Field(
        None,
        description="Logical table name. If unset, derived from filename (for file inputs)."
    )
    normalize_table_names: bool = Field(
        True,
        description="Whether to normalize table names to snake_case."
    )
    recursive: bool = Field(
        False,
        description="If `input_path` is a directory, recurse into subdirectories."
    )
    file_pattern: str = Field(
        "*.csv",
        description="Glob pattern for selecting files in a directory."
    )
    table_name_from_file: bool = Field(
        True,
        description="When processing multiple files, use each filename (minus extension) as its table name."
    )

    entity_fields: Optional[List[EntityField]] = Field(
        None,
        description="List of specific table/field pairs to canonicalize."
    )
    semantic_fields: Optional[List[str]] = Field(
        None,
        description="Column names to include when building semantic embeddings."
    )
    use_other_fields_as_metadata: bool = Field(
        False,
        description="Treat non-entity columns as metadata in the canonical entity list."
    )
    num_rows: Optional[int] = Field(
        None,
        description="Maximum number of rows to process from each source."
    )

    generate_canonical_entities: bool = Field(
        True,
        description="Whether to build the canonical entity list."
    )
    generate_schema: bool = Field(
        False,
        description="Whether to infer and emit a database schema."
    )
    generate_embeddings: bool = Field(
        False,
        description="Whether to compute embeddings for canonical entities."
    )
    save_processed_data: bool = Field(
        False,
        description="Whether to save a cleaned copy of the input data."
    )

    schema_database_type: DatabaseType = Field(
        "duckdb",
        description="Target SQL dialect for schema generation."
    )
    clean_field_names: bool = Field(
        True,
        description="Whether to clean column names (snake_case, strip special chars)."
    )
    verbose: Optional[bool] = Field(
        None,
        description="If set, overrides the CanonMap default_verbose; otherwise inherits it."
    )

    @root_validator(pre=True)
    def _default_output_path(cls, values):
        inp = values.get("input_path")
        out = values.get("output_path")
        if out is None and isinstance(inp, (str, Path)):
            p = Path(inp)
            if p.is_file():
                values["output_path"] = p.parent
        return values