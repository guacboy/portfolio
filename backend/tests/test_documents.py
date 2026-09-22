from pathlib import Path

from app.rag.documents import load_resume_documents


def test_loads_every_markdown_file(sample_resume_dir):
    docs = load_resume_documents(sample_resume_dir)
    sources = {d.metadata["source"] for d in docs}
    assert sources == {"about.md", str(Path("projects") / "cat-sim.md")}


def test_preserves_frontmatter_metadata(sample_resume_dir):
    docs = load_resume_documents(sample_resume_dir)
    about_doc = next(d for d in docs if d.metadata["source"] == "about.md")

    assert about_doc.metadata["type"] == "about"
    assert about_doc.metadata["title"] == "Summary"
    assert "cat-related simulations" in about_doc.page_content


def test_chunk_index_is_recorded_in_metadata(sample_resume_dir):
    docs = load_resume_documents(sample_resume_dir)
    assert all("chunk" in d.metadata for d in docs)


def test_empty_directory_returns_no_documents(tmp_path):
    assert load_resume_documents(tmp_path) == []
