# canonmap/models/artifact_unpacking_request.py

from pathlib import Path
from typing import Union, Optional
from pydantic import BaseModel, Field, ConfigDict

class ArtifactUnpackingRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

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