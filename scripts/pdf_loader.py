## scripts/pdf_loader.py

import fitz  
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_chunks = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text.strip():
            text_chunks.append({
                "content": text.strip(),
                "page": page_num
            })
    return text_chunks

def load_all_pdfs(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            text_pages = extract_text_from_pdf(full_path)
            for page in text_pages:
                documents.append({
                    "content": page["content"],
                    "source": filename,
                    "page": page["page"],
                    "title": filename.replace(".pdf", "")
                })
    return documents
