# canonmap/exceptions.py

class CanonMapError(Exception):
    """Base exception for all canonmap errors."""

class ArtifactGenerationError(CanonMapError):
    """Raised when something goes wrong during artifact generation."""

class ArtifactUnpackingError(CanonMapError):
    """Raised when unpacking of artifacts fails."""

class EntityMappingError(CanonMapError):
    """Raised when entity mapping encounters an error."""