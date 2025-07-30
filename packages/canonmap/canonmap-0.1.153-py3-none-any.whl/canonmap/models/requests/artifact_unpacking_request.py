# canonmap/models/requests/artifact_unpacking_request.py
# Request model for artifact unpacking operations

from pathlib import Path
from typing import Union, Optional
from pydantic import BaseModel, Field, ConfigDict

class ArtifactUnpackingRequest(BaseModel):
    """Configuration for unpacking generated artifacts into readable formats.
    
    This model defines parameters for converting binary artifact files into
    human-readable formats like CSV and JSON.

    Args:
        input_path: Directory or file containing artifacts to unpack
        output_path: Directory where unpacked files will be written
        verbose: Override CanonMap's verbosity setting (default: None)
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "input_path": "artifacts/",
                    "output_path": "unpacked/"
                }
            ]
        }
    )

    input_path: Union[str, Path] = Field(
        ...,
        description="Directory or file containing the artifacts to unpack."
    )
    output_path: Union[str, Path] = Field(
        ...,
        description="Directory where unpacked CSV/JSON files will be written."
    )
    verbose: Optional[bool] = Field(
        None,
        description="If set, overrides the CanonMap default_verbose; otherwise inherits it."
    )