from pathlib import Path
from typing import Dict
from canonmap.utils.logger import get_logger

logger = get_logger("find_artifact_files")

def find_artifact_files(base_path: str) -> Dict[str, Path]:
    """
    Given a directory path, locate exactly one of each:
      - *_schema.pkl
      - *_canonical_entities.pkl
      - *_canonical_entity_embeddings.npz

    Returns a dict mapping keys to Path objects.
    Raises if the directory doesn't exist or any of the three files are missing.
    """
    in_dir = Path(base_path)
    if not in_dir.is_dir():
        logger.error(f"Path {base_path!r} is not a directory")
        raise ValueError(f"Path {base_path!r} is not a directory")

    schema_files = list(in_dir.glob("*_schema.pkl"))
    entity_files = list(in_dir.glob("*_canonical_entities.pkl"))
    embed_files  = list(in_dir.glob("*_canonical_entity_embeddings.npz"))

    missing = []
    if not schema_files:
        missing.append("*_schema.pkl")
    if not entity_files:
        missing.append("*_canonical_entities.pkl")
    if not embed_files:
        missing.append("*_canonical_entity_embeddings.npz")

    if missing:
        logger.error(f"Missing required artifact files: {', '.join(missing)}")
        raise FileNotFoundError(f"Missing required artifact files: {', '.join(missing)}")

    result: Dict[str, Path] = {
        "schema": schema_files[0],
        "canonical_entities": entity_files[0],
        "canonical_entity_embeddings": embed_files[0],
    }

    logger.info("Found all required artifact files in %r", base_path)
    return result