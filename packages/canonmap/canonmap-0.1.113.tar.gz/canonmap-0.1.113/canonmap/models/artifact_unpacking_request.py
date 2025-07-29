# canonmap/models/unpack_artifact_request.py

from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field

class ArtifactUnpackingRequest(BaseModel):
    input_path: Path = Field(
        ...,
        description="Directory containing the *_canonical_entities.pkl, *_schema.pkl, and *_processed_data.pkl files to unpack."
    )
    output_path: Optional[Path] = Field(
        None,
        description="Where to write the JSON/CSV outputs. Defaults to the input_path if omitted."
    )
    verbose: bool = Field(
        False,
        description="Enable verbose logging for debugging."
    )