# rag_inference.py

import pickle
import faiss
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "embeddings/faiss_index.index"
METADATA_PATH = "embeddings/metadata.pkl"

# ------- Load components once -------

embedder = SentenceTransformer(EMBED_MODEL)
llm = Ollama(model="mistral",
        base_url="http://host.docker.internal:11434")

# ------- Load FAISS + metadata -------

with open(METADATA_PATH, "rb") as f:
    METADATA = pickle.load(f)

FAISS_INDEX = faiss.read_index(FAISS_INDEX_PATH)

# ------- Core retrieval function -------

def rag_retrieve(question, top_k=3):
    """Return top-k document chunks."""
    vec = embedder.encode([question])
    D, I = FAISS_INDEX.search(vec, top_k)

    results = []
    for idx in I[0]:
        chunk = METADATA[idx]
        results.append({
            "content": chunk["content"],
            "source": chunk["source"],
            "title": chunk["title"],
            "page": chunk["page"]
        })
    return results

# ------- Prompt builder -------

def build_rag_prompt(question, chunks):
    context = "\n\n".join(
        f"[{i+1}] Title: {c['title']} (page {c['page']})\n{c['content']}"
        for i, c in enumerate(chunks)
    )

    return f"""
You are a helpful assistant. Use ONLY the CONTEXT below to answer the question.

### CONTEXT:
{context}

### QUESTION:
{question}

### ANSWER:
"""

# ------- RAG main entry point -------

def rag_answer(question, top_k=3):
    """
    Main RAG function that:
    1. retrieves chunks
    2. builds prompt
    3. calls Ollama mistral
    4. returns answer text
    """
    chunks = rag_retrieve(question, top_k)
    prompt = build_rag_prompt(question, chunks)
    answer = llm.invoke(prompt)
    return {
        "answer": answer.strip(),
        "chunks": chunks
    }

#  MCP Tool Enrty

def run_rag(query: str) -> dict:
    """
    MCP tool will call this function
    must return JSON-like dict
    """
    result = rag_answer(query)
    return result

if __name__ == "__main__":
    q = input("Question: ")
    print(rag_answer(q))
