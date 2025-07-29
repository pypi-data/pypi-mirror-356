from docrag._version import __version__
from docrag.core.doc_rag import DocRag
from docrag.core.document import Document, Page
from docrag.core.vector_store import VectorStore
from docrag.utils.log_utils import setup_logging

setup_logging()

__all__ = ["DocRag", "Document", "Page", "VectorStore", "__version__"]
