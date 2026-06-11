import io
import os
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()


def extract_text(filename: str, file_bytes: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n\n".join(p.extract_text() or "" for p in reader.pages)
    elif ext in (".docx", ".doc"):
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    else:
        return file_bytes.decode("utf-8", errors="replace")


def save_upload(project_id: str, filename: str, file_bytes: bytes) -> str:
    path = Path(settings.upload_dir) / project_id
    path.mkdir(parents=True, exist_ok=True)
    dest = path / filename
    dest.write_bytes(file_bytes)
    return str(dest)


def store_embeddings(project_id: str, text: str):
    try:
        import chromadb
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        client = chromadb.PersistentClient(path=settings.chromadb_path)
        col = client.get_or_create_collection(f"project_{project_id}")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)
        if chunks:
            col.add(
                documents=chunks,
                ids=[f"{project_id}_{i}" for i in range(len(chunks))],
            )
    except Exception as e:
        print(f"Embedding store failed (non-fatal): {e}")
