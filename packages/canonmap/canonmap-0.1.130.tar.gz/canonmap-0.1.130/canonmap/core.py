# canonmap/core.py

import logging
from canonmap.container import Container
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest

def _apply_verbosity(verbose: bool):
    """
    Configure root logger so that INFO+ will be printed if verbose=True,
    otherwise only WARNING+.
    """
    level = logging.INFO if verbose else logging.WARNING
    # If no handlers are configured yet, set up a basic one:
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            level=level
        )
    else:
        logging.getLogger().setLevel(level)

class CanonMap:
    """
    Facade with a global verbosity default, overridable per-call.
    """
    def __init__(self, artifacts_path: str, verbose: bool = False):
        # store the global default
        self.default_verbose = verbose
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest):
        # decide final verbosity
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(verbose)
        return self.container.generation_controller().run(config)

    def unpack(self, config: ArtifactUnpackingRequest):
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(verbose)
        return self.container.unpacking_controller().run(config)

    def map_entities(self, config: EntityMappingRequest):
        # default artifacts_path if none provided
        if config.artifacts_path is None:
            config.artifacts_path = self.container.base_artifacts_path
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(verbose)
        return self.container.mapping_controller().run(config)