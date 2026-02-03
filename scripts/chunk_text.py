# scripts/chunk_text.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["content"]):
            chunks.append({
                "content": chunk,
                "source": doc["source"],
                "title": doc["title"],
                "page": doc["page"]
            })
    return chunks
