# canonmap/utils/find_unpackable_files.py

from pathlib import Path
from typing import Dict
from canonmap.utils.logger import get_logger

logger = get_logger("find_unpackable_files")

def find_unpackable_files(base_path: str) -> Dict[str, Path]:
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
    for pat, key in patterns:
        hits = list(p.glob(pat))
        if hits:
            out[key] = hits[0]
        else:
            # schema & entities are required - processed_data optional
            if key in ("schema", "canonical_entities"):
                raise FileNotFoundError(f"Could not find any {pat!r} in {base_path}")
    logger.info("Unpackable files found: %s", list(out.keys()))
    return out