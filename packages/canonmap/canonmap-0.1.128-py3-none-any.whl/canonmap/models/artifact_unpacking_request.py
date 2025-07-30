# canonmap/models/artifact_unpacking_request.py

from pathlib import Path
from typing import Union
from pydantic import BaseModel, Field

class ArtifactUnpackingRequest(BaseModel):
    input_path: Union[str, Path] = Field(
        ...,
        description="Directory or file containing the artifacts to unpack."
    )
    output_path: Path = Field(
        ...,
        description="Directory where unpacked CSV/JSON files will be written."
    )
    verbose: bool = Field(
        False,
        description="Enable verbose logging during unpacking."
    )

    class Config:
        extra = "forbid"