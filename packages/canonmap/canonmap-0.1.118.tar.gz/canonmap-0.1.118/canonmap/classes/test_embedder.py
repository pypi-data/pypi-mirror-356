import time
import psutil
import numpy as np
from canonmap.classes.embedder import Embedder

TEST_SIZES = [64, 128, 256, 512]
NUM_TEXTS = 5000  # total texts to embed
TEXT_SAMPLE = '{"artist": "Vance Joy"}'  # representative short input

texts = [TEXT_SAMPLE] * NUM_TEXTS
print(f"Running benchmark on {NUM_TEXTS} short texts...\n")

for batch_size in TEST_SIZES:
    try:
        print(f"🔍 Testing batch size: {batch_size}")
        embedder = Embedder(batch_size=batch_size)

        start_time = time.time()
        embeddings = embedder.embed_texts(texts)
        end_time = time.time()

        memory_used = psutil.Process().memory_info().rss / 1e9
        duration = round(end_time - start_time, 2)

        print(f"✅ Success — Time: {duration}s | Shape: {embeddings.shape} | Memory Used: {memory_used:.2f} GB\n")

    except Exception as e:
        print(f"❌ Failed at batch size {batch_size}: {e}\n")