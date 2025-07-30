# canonmap/controllers/unpacking.py

from canonmap.models.artifact_unpacking_request import ArtifactUnpackingRequest
from canonmap.services.artifact_unpacker import ArtifactUnpacker

class UnpackingController:
    """
    Controller for unpacking pre‐generated artifacts into human‐readable CSV/JSON.
    """

    def __init__(self, artifact_files: dict):
        # artifact_files: a dict mapping artifact names → Path objects
        self.artifact_files = artifact_files

    def run(self, config: ArtifactUnpackingRequest):
        """
        Read .pkl artifacts from `artifact_files` and write them to `config.output_path`.
        """
        unpacker = ArtifactUnpacker(artifact_files=self.artifact_files)
        return unpacker.unpack_artifacts(config)