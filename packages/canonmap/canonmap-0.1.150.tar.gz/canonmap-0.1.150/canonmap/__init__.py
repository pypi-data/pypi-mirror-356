# canonmap/__init__.py

from .core import CanonMap

# models - updated to use new organized structure
from .models.requests.artifact_generation_request import ArtifactGenerationRequest, EntityField
from .models.requests.artifact_unpacking_request import ArtifactUnpackingRequest
from .models.requests.entity_mapping_request import EntityMappingRequest, TableFieldFilter
from .models.responses.artifact_generation_response import ArtifactGenerationResponse
from .models.responses.entity_mapping_response import EntityMappingResponse, MatchItem, SingleMapping

__all__ = [
    "CanonMap",
    "ArtifactGenerationRequest", "EntityField",
    "ArtifactUnpackingRequest",
    "EntityMappingRequest", "TableFieldFilter",
    "ArtifactGenerationResponse",
    "EntityMappingResponse", "MatchItem", "SingleMapping",
]