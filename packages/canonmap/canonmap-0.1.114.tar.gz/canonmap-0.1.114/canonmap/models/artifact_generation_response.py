# canonmap/models/artifact_response.py

from typing import Dict
from pydantic import BaseModel, Field

class ArtifactGenerationResponse(BaseModel):
    message: str = Field(..., description="Summary of the operation")
    paths: Dict[str, Dict[str, str]] = Field(..., description="Paths to generated artifacts for each table")