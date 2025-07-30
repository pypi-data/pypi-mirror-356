from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.services.artifact_unpacker import ArtifactUnpacker

class UnpackingController:
    """
    Controller for unpacking pre-generated artifacts into JSON/CSV.
    """
    def __init__(self, unpack_finder):
        # unpack_finder: Callable[[str], Dict[str, Path]]
        self.unpack_finder = unpack_finder

    def run(self, config: ArtifactUnpackingRequest):
        # 1) resolve the actual pickle files we need
        artifact_paths = self.unpack_finder(str(config.input_path))

        # 2) hand off to the existing service
        unpacker = ArtifactUnpacker(artifact_files=artifact_paths)
        return unpacker.unpack_artifacts(config)