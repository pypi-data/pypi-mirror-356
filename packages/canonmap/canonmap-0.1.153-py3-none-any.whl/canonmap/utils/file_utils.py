# canonmap/utils/file_utils.py

from pathlib import Path
from typing import Dict
from canonmap.utils.logger import get_logger

logger = get_logger("file_utils")

def find_artifact_files(base_path: str) -> Dict[str, Path]:
    """
    Find the core artifact files needed for entity mapping.
    Returns schema, canonical entities, and embeddings files.
    """
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

def find_unpackable_files(base_path: str) -> Dict[str, Path]:
    """
    Find files that can be unpacked into human-readable formats.
    Returns schema, canonical entities, and optionally processed data files.
    """
    p = Path(base_path)
    if not p.is_dir():
        raise ValueError(f"{base_path!r} is not a directory")

    # grab everything we unpack into human formats
    patterns = [
        ("*_schema.pkl",                 "schema"),
        ("*_canonical_entities.pkl",     "canonical_entities"),
        ("*_processed_data.pkl",         "processed_data"),
    ]
    out: Dict[str, Path] = {}
    logger.debug(f"Searching for unpackable files in {base_path}")
    for pat, key in patterns:
        hits = list(p.glob(pat))
        logger.debug(f"Pattern {pat!r} found {len(hits)} files: {[str(h) for h in hits]}")
        if hits:
            out[key] = hits[0]
            logger.debug(f"Added {key}: {hits[0]}")
        else:
            # schema & entities are required - processed_data optional
            if key in ("schema", "canonical_entities"):
                raise FileNotFoundError(f"Could not find any {pat!r} in {base_path}")
    logger.info("Unpackable files found: %s", list(out.keys()))
    return out 