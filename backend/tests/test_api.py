from fastapi.testclient import TestClient

import app.api.chat as chat_api
from app.main import app
from app.rag.chat import ChatResult

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_answer_and_sources(monkeypatch):
    monkeypatch.setattr(
        chat_api,
        "answer",
        lambda message: ChatResult(answer="Dylan builds things.", sources=["about.md"]),
    )

    response = client.post("/chat", json={"message": "What does Dylan do?"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Dylan builds things.", "sources": ["about.md"]}


def test_chat_endpoint_rejects_empty_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_endpoint_rejects_overlong_message():
    response = client.post("/chat", json={"message": "a" * 1001})
    assert response.status_code == 422
