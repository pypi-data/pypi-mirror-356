# canonmap/core.py

import logging
from canonmap.container import Container
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest

def _apply_verbosity(verbose: bool):
    """
    Remove all existing handlers, then configure exactly one StreamHandler
    at INFO level if verbose=True, else WARNING.
    """
    level = logging.INFO if verbose else logging.WARNING

    root = logging.getLogger()
    # 1) remove all handlers (clears both root and propagated child handlers)
    for h in root.handlers[:]:
        root.removeHandler(h)

    # 2) (re)configure exactly one basic handler
    logging.basicConfig(
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        level=level,
        force=True,   # ensure the above format+level are applied
    )

class CanonMap:
    """
    Facade with a global verbosity default, overridable per-call.
    """
    def __init__(self, artifacts_path: str, verbose: bool = False):
        self.default_verbose = verbose
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest):
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(verbose)
        return self.container.generation_controller().run(config)

    def unpack(self, config: ArtifactUnpackingRequest):
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(verbose)
        return self.container.unpacking_controller().run(config)

    def map_entities(self, config: EntityMappingRequest):
        if config.artifacts_path is None:
            config.artifacts_path = self.container.base_artifacts_path
        verbose = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(verbose)
        return self.container.mapping_controller().run(config)