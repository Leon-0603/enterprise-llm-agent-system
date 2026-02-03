# main_prepare_chunks.py

import json
from scripts.pdf_loader import load_all_pdfs
from scripts.chunk_text import chunk_documents
from pathlib import Path

if __name__ == "__main__":
    # 1. Load data
    raw_docs = load_all_pdfs("adv_paper")

    # 2. Chunk 
    chunks = chunk_documents(raw_docs)

    # 3. Save JSONL format
    output_path = Path("data/chunks.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            json.dump(chunk, f, ensure_ascii=False)
            f.write("\n")

    print(f" complete： {len(chunks)}  chunks save to {output_path}")
