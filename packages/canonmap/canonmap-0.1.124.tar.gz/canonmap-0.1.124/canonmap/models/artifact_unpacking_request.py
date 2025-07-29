# File: canonmap/models/artifact_unpacking_request.py

from pathlib import Path
from pydantic import BaseModel, Field

class ArtifactUnpackingRequest(BaseModel):
    output_path: Path = Field(
        ...,
        description="Directory where JSON/CSV outputs will be written."
    )
    verbose: bool = Field(
        False,
        description="Enable verbose logging for debugging."
    )