# canonmap/cli.py
import click
from sentence_transformers import SentenceTransformer

@click.command()
@click.argument("model", default="all-MiniLM-L6-v2")
def download_model(model):
    """
    Download the given Sentence-Transformer into the local HF cache.
    """
    click.echo(f"⏬ Downloading {model}…")
    # this will reach out to HF and cache everything locally
    SentenceTransformer(model)
    click.echo(f"✅ Cached {model} successfully.")

# in setup.py or pyproject.toml under [tool.poetry.scripts] / entry_points:
#   canonmap-download-model = canonmap.cli:download_model