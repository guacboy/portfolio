from app.core.config import settings
from app.rag.documents import load_resume_documents
from app.rag.index import build_index, load_index, save_index


def test_build_index_and_similarity_search_finds_relevant_doc(sample_resume_dir):
    docs = load_resume_documents(sample_resume_dir)
    index = build_index(docs)

    results = index.similarity_search_with_score("Tell me about cats chasing lasers", k=1)

    assert results
    doc, _ = results[0]
    assert "cat" in doc.page_content.lower()


def test_save_and_load_index_roundtrip(tmp_path, sample_resume_dir, monkeypatch):
    docs = load_resume_documents(sample_resume_dir)
    index = build_index(docs)

    monkeypatch.setattr(settings, "index_dir", tmp_path / "index")
    save_index(index)

    assert (tmp_path / "index").exists()

    loaded = load_index()
    results = loaded.similarity_search("cats", k=1)
    assert results
