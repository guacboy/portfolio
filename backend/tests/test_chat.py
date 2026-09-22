from unittest.mock import MagicMock

from app.rag import chat as chat_module


class FakeDoc:
    def __init__(self, content, source):
        self.page_content = content
        self.metadata = {"source": source}


class FakeIndex:
    def __init__(self, results):
        self._results = results

    def similarity_search_with_score(self, query, k):
        return self._results


def test_refuses_when_no_results(monkeypatch):
    monkeypatch.setattr(chat_module, "_get_index", lambda: FakeIndex([]))

    result = chat_module.answer("anything")

    assert result.answer == chat_module.REFUSAL
    assert result.sources == []


def test_refuses_when_best_match_is_too_far(monkeypatch):
    far_doc = FakeDoc("irrelevant content", "about.md")
    threshold = chat_module.settings.retrieval_distance_threshold
    monkeypatch.setattr(
        chat_module, "_get_index", lambda: FakeIndex([(far_doc, threshold + 0.1)])
    )
    generate_mock = MagicMock()
    monkeypatch.setattr(chat_module, "generate", generate_mock)

    result = chat_module.answer("what's the weather today?")

    assert result.answer == chat_module.REFUSAL
    generate_mock.assert_not_called()


def test_answers_when_match_is_within_threshold(monkeypatch):
    doc = FakeDoc("Dylan built a chess bot with PyTorch.", "projects/mirror-ai-chess-bot.md")
    threshold = chat_module.settings.retrieval_distance_threshold
    monkeypatch.setattr(
        chat_module, "_get_index", lambda: FakeIndex([(doc, threshold - 0.1)])
    )
    monkeypatch.setattr(
        chat_module, "generate", lambda system, user: "Dylan built a chess bot."
    )

    result = chat_module.answer("What did Dylan build with PyTorch?")

    assert result.answer == "Dylan built a chess bot."
    assert result.sources == ["projects/mirror-ai-chess-bot.md"]


def test_context_and_question_are_passed_to_generate(monkeypatch):
    doc = FakeDoc("Dylan's skills include Python and PyTorch.", "skills.md")
    threshold = chat_module.settings.retrieval_distance_threshold
    monkeypatch.setattr(
        chat_module, "_get_index", lambda: FakeIndex([(doc, threshold - 0.1)])
    )
    generate_mock = MagicMock(return_value="answer")
    monkeypatch.setattr(chat_module, "generate", generate_mock)

    chat_module.answer("What are Dylan's skills?")

    system_prompt, user_prompt = generate_mock.call_args[0]
    assert chat_module.REFUSAL in system_prompt
    assert "Dylan's skills include Python and PyTorch." in user_prompt
    assert "What are Dylan's skills?" in user_prompt
