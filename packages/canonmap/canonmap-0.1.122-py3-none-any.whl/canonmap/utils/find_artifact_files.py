from pathlib import Path
from canonmap.utils.logger import get_logger

logger = get_logger("find_artifact_files")

def find_artifact_files(file_path: str) -> dict:
    """
    Given a file path, this function looks for *_schema.pkl, *_canonical_entities.pkl, and *_canonical_entity_embeddings.npz files
    and returns their paths as a dict. Raises an exception if any are missing.
    """
    in_dir = Path(file_path)
    if not in_dir.is_dir():
        logger.error(f"Path {file_path} is not a directory")
        raise ValueError(f"Path {file_path} is not a directory")

    schema_files = list(in_dir.glob("*_schema.pkl"))
    canonical_entities_files = list(in_dir.glob("*_canonical_entities.pkl"))
    canonical_embeddings_files = list(in_dir.glob("*_canonical_entity_embeddings.npz"))

    if not schema_files or not canonical_entities_files or not canonical_embeddings_files:
        missing = []
        if not schema_files:
            missing.append("*_schema.pkl")
        if not canonical_entities_files:
            missing.append("*_canonical_entities.pkl")
        if not canonical_embeddings_files:
            missing.append("*_canonical_entity_embeddings.npz")
        logger.error(f"Missing required artifact files: {', '.join(missing)}")
        raise FileNotFoundError(f"Missing required artifact files: {', '.join(missing)}")

    result = {
        "schema": str(schema_files[0]),
        "canonical_entities": str(canonical_entities_files[0]),
        "canonical_entity_embeddings": str(canonical_embeddings_files[0]),
    }
    logger.info(f"Found artifact files: {result}")
    return result