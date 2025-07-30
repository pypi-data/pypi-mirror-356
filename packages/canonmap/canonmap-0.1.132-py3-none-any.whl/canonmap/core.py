# canonmap/core.py

import logging
from typing import Optional, Dict, Any

from canonmap.container import Container
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest
from canonmap.utils.logger import _loggers, get_logger

logger = get_logger("core")

def _apply_verbosity(verbose: bool):
    """
    Flip the logging level on both the root logger (for third-party
    libs) and all of our colored loggers in _loggers.
    """
    level = logging.INFO if verbose else logging.WARNING

    # 1) root logger
    logging.getLogger().setLevel(level)
    # 2) all of our package loggers
    for lg in _loggers.values():
        lg.setLevel(level)


class CanonMap:
    """
    Public façade for canonmap functionality.
    Honors a global default_verbose, overridable per-call via model.verbose.
    """
    def __init__(self, artifacts_path: str, verbose: bool = False):
        self.default_verbose = verbose
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        # choose verbosity: per-request if set, else global default
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting generation (verbose={v})")
        return self.container.generation_controller().run(config)

    def unpack(self, config: ArtifactUnpackingRequest) -> Dict[str, Any]:
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting unpack (verbose={v})")
        return self.container.unpacking_controller().run(config)

    def map_entities(self, config: EntityMappingRequest) -> Any:
        # default artifacts_path if caller omitted it
        if config.artifacts_path is None:
            config.artifacts_path = self.container.base_artifacts_path

        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting mapping (verbose={v}) against '{config.artifacts_path}'")
        return self.container.mapping_controller().run(config)