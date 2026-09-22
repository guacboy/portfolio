from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model_name)


def build_index(documents: list[Document]) -> FAISS:
    return FAISS.from_documents(documents, get_embeddings())


def save_index(index: FAISS) -> None:
    settings.index_dir.mkdir(parents=True, exist_ok=True)
    index.save_local(str(settings.index_dir))


def load_index() -> FAISS:
    return FAISS.load_local(
        str(settings.index_dir),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )
