from unittest.mock import MagicMock

import pytest

from app.rag import llm as llm_module


def test_generate_sends_system_and_user_messages(monkeypatch):
    fake_llm = MagicMock()
    fake_llm.create_chat_completion.return_value = {
        "choices": [{"message": {"content": "  Hello there  "}}]
    }
    monkeypatch.setattr(llm_module, "get_llm", lambda: fake_llm)

    result = llm_module.generate("system prompt", "user prompt")

    assert result == "Hello there"
    _, kwargs = fake_llm.create_chat_completion.call_args
    assert kwargs["messages"] == [
        {"role": "system", "content": "system prompt"},
        {"role": "user", "content": "user prompt"},
    ]


@pytest.mark.slow
def test_generate_with_real_local_model():
    result = llm_module.generate(
        "You are a helpful assistant.",
        "Reply with only the word: test",
    )
    assert isinstance(result, str)
    assert result
