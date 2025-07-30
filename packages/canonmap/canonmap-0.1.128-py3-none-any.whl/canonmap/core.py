from canonmap.container import Container
from canonmap.models.artifact_generation_request import ArtifactGenerationRequest
from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.models.entity_mapping_request import EntityMappingRequest

class CanonMap:
    def __init__(self, artifacts_path: str):
        self.container = Container(artifacts_path)

    def generate(self, config: ArtifactGenerationRequest):
        return self.container.generation_controller().run(config)

    def unpack(self, config: ArtifactUnpackingRequest):
        return self.container.unpacking_controller().run(config)

    def map_entities(self, config: EntityMappingRequest):
        return self.container.mapping_controller().run(config)