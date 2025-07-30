# canonmap/utils/find_artifact_files.py
from pathlib import Path
from typing import Dict
from canonmap.utils.logger import get_logger

logger = get_logger("find_artifact_files")

def find_artifact_files(base_path: str) -> Dict[str, Path]:
    p = Path(base_path)
    if not p.is_dir():
        raise ValueError(f"{base_path!r} is not a directory")
    schema   = list(p.glob("*_schema.pkl"))
    entities = list(p.glob("*_canonical_entities.pkl"))
    embs     = list(p.glob("*_canonical_entity_embeddings.npz"))

    missing = []
    if not schema:   missing.append("*_schema.pkl")
    if not entities: missing.append("*_canonical_entities.pkl")
    if not embs:     missing.append("*_canonical_entity_embeddings.npz")
    if missing:
        logger.error("Missing: %s", missing)
        raise FileNotFoundError(f"Missing artifacts: {missing}")

    return {
        "schema":   schema[0],
        "canonical_entities": entities[0],
        "canonical_entity_embeddings": embs[0],
    }