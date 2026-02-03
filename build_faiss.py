# build_faiss.py

import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

CHUNKS_FILE = "data/chunks.jsonl"
FAISS_INDEX_PATH = "embeddings/faiss_index.index"
METADATA_PATH = "embeddings/metadata.pkl"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def build_faiss_index(chunks, model_name):
    model = SentenceTransformer(model_name)
    texts = [chunk["content"] for chunk in chunks]

    print(f" Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings

if __name__ == "__main__":
    Path("embeddings").mkdir(exist_ok=True)

    print("load chunks")
    chunks = load_chunks(CHUNKS_FILE)

    index, embeddings = build_faiss_index(chunks, EMBED_MODEL)

    print("save FAISS index")
    faiss.write_index(index, FAISS_INDEX_PATH)

    print("save metadata")
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print("FAISS complete")
