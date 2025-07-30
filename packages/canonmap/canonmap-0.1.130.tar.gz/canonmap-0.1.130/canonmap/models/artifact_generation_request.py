# canonmap/models/artifact_generation_request.py

from pathlib import Path
from typing import Optional, List, Dict, Union, Literal, Any
from pydantic import BaseModel, Field, root_validator, ConfigDict
import pandas as pd

DatabaseType = Literal["duckdb", "sqlite", "bigquery", "mariadb", "mysql", "postgresql"]

class EntityField(BaseModel):
    table_name: str = Field(..., description="Name of the table containing the entity field.")
    field_name: str = Field(..., description="Name of the field to canonicalize.")

class ArtifactGenerationRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    input_path: Union[Path, pd.DataFrame, Dict[str, Any]] = Field(
        ...,
        description="Path (file or directory), DataFrame, or dict convertible to DataFrame."
    )
    output_path: Optional[Path] = Field(None, description="Where to write artifacts.")
    source_name: str = Field("data", description="Logical source name.")
    table_name: Optional[str] = Field(None, description="Logical table name override.")
    normalize_table_names: bool = Field(True, description="Snake-case table names?")
    recursive: bool = Field(False, description="Recurse into directories?")
    file_pattern: str = Field("*.csv", description="Glob for files when dir input.")
    table_name_from_file: bool = Field(True, description="Use filename as table name?")
    entity_fields: Optional[List[EntityField]] = Field(None, description="Which fields to canonicalize.")
    semantic_fields: Optional[List[str]] = Field(None, description="Columns for embeddings.")
    use_other_fields_as_metadata: bool = Field(False, description="Use other cols as metadata?")
    num_rows: Optional[int] = Field(None, description="Row limit per table.")
    generate_canonical_entities: bool = Field(True, description="Build canonical entities?")
    generate_schema: bool = Field(False, description="Infer and emit DB schema?")
    generate_embeddings: bool = Field(False, description="Compute embeddings?")
    save_processed_data: bool = Field(False, description="Save cleaned data?")
    schema_database_type: DatabaseType = Field("duckdb", description="SQL dialect for schema.")
    clean_field_names: bool = Field(True, description="Clean column names?")
    verbose: Optional[bool] = Field(
        None,
        description="Override global verbosity. If unset, uses CanonMap default."
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