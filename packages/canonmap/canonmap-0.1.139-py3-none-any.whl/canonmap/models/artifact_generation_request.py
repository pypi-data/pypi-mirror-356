# canonmap/models/artifact_generation_request.py

from pathlib import Path
from typing import Union, Optional, List, Dict, Literal, Any
from pydantic import BaseModel, Field, root_validator, ConfigDict

DatabaseType = Literal["duckdb", "sqlite", "bigquery", "mariadb", "mysql", "postgresql"]

class EntityField(BaseModel):
    table_name: str
    field_name: str

class ArtifactGenerationRequest(BaseModel):
    # allow Path + arbitrary extras, forbid unknown fields:
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    # <-- Note: NO pandas.DataFrame here
    input_path: Union[Path, str, Dict[str, Any]] = Field(
        ...,
        description=(
            "Path (file or directory) to CSV/JSON data, "
            "or a dict convertible to a DataFrame."
        )
    )
    output_path: Optional[Path] = Field(None)
    source_name: str = Field("data")
    table_name: Optional[str] = None
    normalize_table_names: bool = Field(True)

    recursive: bool = Field(False)
    file_pattern: str = Field("*.csv")
    table_name_from_file: bool = Field(True)

    entity_fields: Optional[List[EntityField]] = None
    semantic_fields: Optional[List[str]] = None
    use_other_fields_as_metadata: bool = Field(False)
    num_rows: Optional[int] = None

    generate_canonical_entities: bool = Field(True)
    generate_schema: bool = Field(False)
    generate_embeddings: bool = Field(False)
    save_processed_data: bool = Field(False)

    schema_database_type: DatabaseType = Field("duckdb")
    clean_field_names: bool = Field(True)
    verbose: bool = Field(False)

    @root_validator(pre=True)
    def _default_output_path(cls, values):
        inp = values.get("input_path")
        out = values.get("output_path")
        if out is None and isinstance(inp, (str, Path)):
            p = Path(inp)
            if p.is_file():
                values["output_path"] = p.parent
        return values