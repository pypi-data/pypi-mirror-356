import spacy
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

def load_spacy_model(model_name: str = "en_core_web_sm"):
    logger.info(f"Attempting to load spaCy model '{model_name}'")
    try:
        model = spacy.load(model_name)
        logger.info(f"Successfully loaded spaCy model '{model_name}'")
        return model
    except OSError:
        logger.info(f"spaCy model '{model_name}' not found locally; downloading...")
        cmd = [sys.executable, "-m", "spacy", "download", model_name]
        subprocess.run(cmd, check=True)
        logger.info(f"Download complete. Loading spaCy model '{model_name}'...")
        model = spacy.load(model_name)
        logger.info(f"Successfully loaded downloaded spaCy model '{model_name}'")
        return model