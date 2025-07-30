# canonmap/core.py

import logging
from typing import Dict, Any, Optional

from canonmap.container import Container
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest
from canonmap.utils.logger import _loggers, get_logger

logger = get_logger("core")

def _apply_verbosity(verbose: bool):
    """
    Flip the level on the root logger (for stdlib & 3rd-party) and all
    of our own canonmap.* loggers between WARNING and INFO.
    """
    root_level = logging.INFO if verbose else logging.WARNING
    logging.getLogger().setLevel(root_level)

    our_level = logging.INFO if verbose else logging.WARNING
    for lg in _loggers.values():
        lg.setLevel(our_level)

class CanonMap:
    """
    Public façade for canonmap.
    artifacts_path may be None if you only ever call .generate().
    """
    def __init__(self, artifacts_path: Optional[str] = None, verbose: bool = False):
        # global default verbosity
        self.default_verbose = verbose
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting generation (verbose={v})")
        return self.container.generation_controller().run(config)

    def unpack(self, config: ArtifactUnpackingRequest) -> Dict[str, Any]:
        # 1) if user didn’t give an input_path, fall back to the instance-level one
        if config.input_path is None:
            if self.container.base_artifacts_path is None:
                raise ValueError("Cannot unpack: no input_path was provided to CanonMap")
            config.input_path = self.container.base_artifacts_path

        # 2) now toggle verbosity and dispatch
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting unpack (verbose={v})")
        return self.container.unpacking_controller().run(config)

    def map_entities(self, config: EntityMappingRequest) -> Any:
        if config.artifacts_path is None:
            if self.container.base_artifacts_path is None:
                raise ValueError("Cannot map: no artifacts_path was provided to CanonMap")
            config.artifacts_path = self.container.base_artifacts_path
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting mapping (verbose={v})")
        return self.container.mapping_controller().run(config)