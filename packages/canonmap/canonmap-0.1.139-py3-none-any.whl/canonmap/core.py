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
    level = logging.INFO if verbose else logging.WARNING
    logging.getLogger().setLevel(level)
    for lg in _loggers.values():
        lg.setLevel(level)


class CanonMap:
    """
    Public façade for canonmap functionality.
    `artifacts_path` is only required if you plan to call `.unpack()` or `.map_entities()`.
    You can omit it (or leave it at the default ".") if you only need `.generate()`.
    """
    def __init__(self, artifacts_path: Optional[str] = ".", verbose: bool = False):
        self.default_verbose = verbose
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest) -> Dict[str, Any]:
        # generation pipeline never touches artifacts_path
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting generation (verbose={v})")
        return self.container.generation_controller().run(config)

    def unpack(self, config: ArtifactUnpackingRequest) -> Dict[str, Any]:
        # unpack needs an artifacts_path (constructor default "." will be used if omitted)
        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting unpack (verbose={v})")
        return self.container.unpacking_controller().run(config)

    def map_entities(self, config: EntityMappingRequest) -> Any:
        # use per-call path if provided, else fall back to constructor value
        if config.artifacts_path is None:
            config.artifacts_path = self.container.base_artifacts_path

        v = config.verbose if config.verbose is not None else self.default_verbose
        _apply_verbosity(v)
        logger.info(f"Starting mapping (verbose={v}) against '{config.artifacts_path}'")
        return self.container.mapping_controller().run(config)