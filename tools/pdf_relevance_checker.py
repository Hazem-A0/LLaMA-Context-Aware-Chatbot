# tools/pdf_relevance_checker.py
import io
import hashlib
from typing import List, Callable, Optional
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings, OllamaLLM

from langchain.docstore.document import Document
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Module-level singletons owned here
_embeddings = OllamaEmbeddings(model="llama3")
_vector_store: Optional[FAISS] = None

# Persistent cache (hashes) injected by agent_runner
_processed_hashes = set()
_flush_callback: Optional[Callable[[set], None]] = None
_vectorstore_dir: Optional[str] = None

def attach_persistent_cache(cache_set: set, on_flush: Optional[Callable[[set], None]] = None):
    """Attach a persistent cache (set of pdf hashes) and an optional flush callback to save it."""
    global _processed_hashes, _flush_callback
    _processed_hashes = cache_set
    _flush_callback = on_flush

def ensure_vectorstore_ready(vectorstore_dir: str):
    """Load or initialize the FAISS store once and remember where to save."""
    global _vector_store, _vectorstore_dir
    _vectorstore_dir = vectorstore_dir
    try:
        _vector_store = FAISS.load_local(_vectorstore_dir, _embeddings, allow_dangerous_deserialization=True)
    except Exception:
        _vector_store = None  # created on first add

def _save_vectorstore():
    if _vector_store is not None and _vectorstore_dir:
        _vector_store.save_local(_vectorstore_dir)

def _pdf_hash(pdf_bytes: bytes) -> str:
    return hashlib.md5(pdf_bytes).hexdigest()

def _extract_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def _chunk_text(text: str) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    return [Document(page_content=ch) for ch in chunks]

def add_pdf_if_new(pdf_bytes: bytes, vectorstore_dir: Optional[str] = None):
    """
    Idempotently add a PDF to FAISS if not seen before.
    Uses persistent hash cache if attached.
    """
    global _vector_store
    h = _pdf_hash(pdf_bytes)
    if h in _processed_hashes:
        return

    # Extract and embed
    text = _extract_text(pdf_bytes)
    docs = _chunk_text(text)

    if _vector_store is None:
        _vector_store = FAISS.from_documents(docs, _embeddings)
    else:
        _vector_store.add_documents(docs)

    # Persist artifacts
    if vectorstore_dir is not None:
        # allow override; else default to configured dir
        global _vectorstore_dir
        _vectorstore_dir = vectorstore_dir

    _save_vectorstore()
    _processed_hashes.add(h)
    if _flush_callback:
        _flush_callback(_processed_hashes)

def retrieve_relevant_context(query: str, k: int = 4) -> str:
    """Top-k semantic retrieval from FAISS; empty string if store not ready or nothing found."""
    if _vector_store is None:
        return ""
    results = _vector_store.similarity_search(query, k=k)
    return "\n".join(doc.page_content for doc in results if doc and doc.page_content)
