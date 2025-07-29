"""
CanonMap - A Python library for data mapping and canonicalization
"""

__version__ = "0.1.78"

from .core import CanonMap
from .models.artifact_generation_request import ArtifactGenerationRequest
# from .models.artifact_generation_response import ArtifactGenerationResponse

__all__ = [
    "CanonMap", 
    "ArtifactGenerationRequest", 
    # "ArtifactGenerationResponse"
] 