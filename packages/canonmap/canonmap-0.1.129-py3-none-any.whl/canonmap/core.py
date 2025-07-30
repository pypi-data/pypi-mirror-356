# canonmap/core.py

import logging
from canonmap.container import Container
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest

def _set_logging(verbose: bool) -> int:
    """
    Flip logging.disable() appropriately.
    Returns the previous disable‐level so we can restore it later.
    """
    prev = logging.root.manager.disable
    if verbose:
        logging.disable(logging.NOTSET)
    else:
        logging.disable(logging.INFO)
    return prev

class CanonMap:
    """
    Facade with a global verbosity default, overridable per-call.
    """
    def __init__(self, artifacts_path: str, verbose: bool = False):
        self.default_verbose = verbose
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest):
        # decide verbosity: request.verbose if given, else default
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        prev = _set_logging(verbose)
        try:
            return self.container.generation_controller().run(config)
        finally:
            logging.disable(prev)

    def unpack(self, config: ArtifactUnpackingRequest):
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        prev = _set_logging(verbose)
        try:
            return self.container.unpacking_controller().run(config)
        finally:
            logging.disable(prev)

    def map_entities(self, config: EntityMappingRequest):
        if config.artifacts_path is None:
            config.artifacts_path = self.container.base_artifacts_path
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        prev = _set_logging(verbose)
        try:
            return self.container.mapping_controller().run(config)
        finally:
            logging.disable(prev)