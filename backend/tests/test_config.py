from app.core.config import settings


def test_default_paths_point_at_expected_dirs():
    assert settings.resume_data_dir.name == "resume"
    assert settings.index_dir.name == "index"
    assert settings.model_path.suffix == ".gguf"


def test_default_embedding_model():
    assert settings.embedding_model_name == "sentence-transformers/all-MiniLM-L6-v2"


def test_retrieval_defaults_are_sane():
    assert settings.retrieval_top_k > 0
    assert settings.retrieval_distance_threshold > 0
