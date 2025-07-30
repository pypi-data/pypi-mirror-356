# canonmap/controllers/unpacking.py

from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.services.artifact_unpacker import ArtifactUnpacker

class UnpackingController:
    """
    Controller for unpacking pre‐generated artifacts into human‐readable CSV/JSON.
    """

    def __init__(self, file_finder):
        # file_finder: Callable[[str], Dict[str, Path]]
        self.file_finder = file_finder

    def run(self, config: ArtifactUnpackingRequest):
        # 1) re‐discover artifacts in the directory (or file) they sent
        artifacts = self.file_finder(str(config.input_path))

        # 2) hand off to the existing service
        unpacker = ArtifactUnpacker(artifact_files=artifacts)
        return unpacker.unpack_artifacts(config)