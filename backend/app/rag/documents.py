from pathlib import Path

import frontmatter
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings

_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


def load_resume_documents(data_dir: Path | None = None) -> list[Document]:
    """Load every markdown source doc under data_dir into chunked LangChain Documents."""
    root = data_dir or settings.resume_data_dir
    documents: list[Document] = []

    for path in sorted(root.rglob("*.md")):
        post = frontmatter.load(path)
        metadata = {**post.metadata, "source": str(path.relative_to(root))}

        for i, chunk in enumerate(_SPLITTER.split_text(post.content.strip())):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={**metadata, "chunk": i},
                )
            )

    return documents
