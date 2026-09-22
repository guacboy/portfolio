"""Build the FAISS index from backend/data/resume/. Run after editing resume content."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.documents import load_resume_documents
from app.rag.index import build_index, save_index


def main() -> None:
    documents = load_resume_documents()
    if not documents:
        raise SystemExit("No source documents found under backend/data/resume/.")

    print(f"Loaded {len(documents)} chunks from resume source documents.")
    index = build_index(documents)
    save_index(index)
    print("Saved FAISS index to backend/data/index/.")


if __name__ == "__main__":
    main()
