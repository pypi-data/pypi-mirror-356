import os
import glob
import uuid
from typing import List, Dict, Any

import PyPDF2
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from tqdm import tqdm

# ---- CONFIG ----
BOOKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../book_data'))
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "test_books_collection_2"  
EMBEDDING_MODEL = "OrlikB/KartonBERT-USE-base-v1"
MIN_CHUNK_SIZE = 800

def extract_text_by_page(pdf_path: str) -> List[Dict[str, Any]]:
    """Extracts text from each page of a PDF, returns list of dicts with text and page number."""
    results = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        for i, page in enumerate(tqdm(reader.pages, desc=f"Extracting pages from {os.path.basename(pdf_path)}", total=num_pages)):
            text = page.extract_text()
            if text and text.strip():
                results.append({
                    'text': text,
                    'page': i + 1
                })
    return results

def semantic_chunk_pages(pages: List[Dict[str, Any]], chunker: SemanticChunker) -> List[Dict[str, Any]]:
    """Chunks the text of each page semantically, returns list of dicts with chunk text and page numbers."""
    chunks = []
    for page in tqdm(pages, desc="Chunking pages", total=len(pages)):
        page_text = page['text']
        page_num = page['page']
        chunk_texts = chunker.split_text(page_text)
        for chunk in chunk_texts:
            chunks.append({
                'text': chunk,
                'pages': [page_num]
            })
    return chunks

def embed_chunks(chunks: List[Dict[str, Any]], embedder: HuggingFaceEmbeddings) -> List[List[float]]:
    texts = [chunk['text'] for chunk in chunks]
    return embedder.embed_documents(texts)

def ensure_collection(client: QdrantClient, collection_name: str, vector_size: int):
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

def main():
    pdf_files = glob.glob(os.path.join(BOOKS_DIR, '*.pdf'))
    if not pdf_files:
        print(f"No PDF files found in {BOOKS_DIR}")
        return

    print(f"Found {len(pdf_files)} PDF files.")
    embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    chunker = SemanticChunker(embeddings=embedder, min_chunk_size=MIN_CHUNK_SIZE)
    client = QdrantClient(url=QDRANT_URL)

    # Determine embedding size
    test_vec = embedder.embed_documents(["test"])[0]
    vector_size = len(test_vec)
    ensure_collection(client, COLLECTION_NAME, vector_size)

    total_uploaded = 0
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"Processing {filename}...")
        pages = extract_text_by_page(pdf_path)
        if not pages:
            print(f"  No extractable text in {filename}")
            continue

        # Join all text into a single corpus
        full_text = "\n".join(page['text'] for page in pages)
        print(f"  Performing semantic chunking on the entire book...")
        chunk_texts = []
        for chunk in tqdm(chunker.split_text(full_text), desc="Semantic chunking", total=None):
            chunk_texts.append(chunk)
        chunks = [
            {
                'text': chunk,
                'pages': [pages[0]['page'], pages[-1]['page']] if pages else []
            }
            for chunk in chunk_texts
        ]
        if not chunks:
            print(f"  No chunks generated for {filename}")
            continue

        md_filename = os.path.splitext(filename)[0] + '_chunks.md'
        md_path = os.path.join(BOOKS_DIR, md_filename)
        with open(md_path, 'w', encoding='utf-8') as md_file:
            for idx, chunk in enumerate(chunks):
                md_file.write(f"--- CHUNK {idx+1} (Page(s): {', '.join(map(str, chunk['pages']))}) ---\n")
                md_file.write(chunk['text'].strip() + '\n\n')
        print(f"  Wrote chunked Markdown to {md_path}")

        embeddings = embed_chunks(chunks, embedder)
        points = []
        print(f"  Embedding and preparing {len(chunks)} chunks...")
        for i, (chunk, vector) in enumerate(tqdm(zip(chunks, embeddings), total=len(chunks), desc=f"Processing chunks for {filename}")):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "filename": filename,
                    "pages": chunk['pages'],
                    "text": chunk['text']
                }
            ))
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"  Uploaded {len(points)} chunks from {filename}")
        total_uploaded += len(points)
    print(f"Done. Uploaded {total_uploaded} chunks in total.")

if __name__ == "__main__":
    main()
