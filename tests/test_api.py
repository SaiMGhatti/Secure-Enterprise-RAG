import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.rag import service
from app.rag.llm import LLMError

client = TestClient(app)


def fake_result(category="HR"):
    return {
        "_source": {
            "document_id": "doc1",
            "category": category,
            "chunk_index": 0,
            "text": "Employees receive 15 vacation days.",
            "metadata": {"file_name": "leave.txt"},
        },
        "rerank_score": 1.0,
    }


def test_ui_is_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "Secure Enterprise RAG" in response.text


def test_query_requires_token():
    assert client.post("/query", json={"query": "hi"}).status_code == 401


def test_query_rejects_unknown_token():
    response = client.post(
        "/query", json={"query": "hi"}, headers={"Authorization": "Bearer nope"}
    )
    assert response.status_code == 401


def test_caller_cannot_choose_own_identity(monkeypatch):
    seen = {}

    def fake_retrieve(query, user):
        seen["user"] = user
        return [fake_result()]

    monkeypatch.setattr(service, "_retrieve", fake_retrieve)
    monkeypatch.setattr(service.llm, "generate", lambda s, u: "15 days [S1]")

    response = client.post(
        "/query",
        json={"query": "vacation?", "departments": ["Finance"], "roles": ["admin"]},
        headers={"Authorization": "Bearer dev-hr-associate"},
    )

    assert response.status_code == 200
    assert seen["user"].departments == ["HR"]
    assert seen["user"].roles == ["employee"]
    body = response.json()
    assert body["answer"] == "15 days [S1]"
    assert body["sources"][0]["file_name"] == "leave.txt"


def test_no_authorized_results_skips_llm(monkeypatch):
    monkeypatch.setattr(service, "_retrieve", lambda q, u: [])

    def boom(*args):
        raise AssertionError("LLM must not be called without authorized context")

    monkeypatch.setattr(service.llm, "generate", boom)

    response = client.post(
        "/query",
        json={"query": "salaries?"},
        headers={"Authorization": "Bearer dev-hr-associate"},
    )

    assert response.status_code == 200
    assert response.json()["sources"] == []


def test_llm_failure_returns_503(monkeypatch):
    monkeypatch.setattr(service, "_retrieve", lambda q, u: [fake_result()])

    def fail(*args):
        raise LLMError("down")

    monkeypatch.setattr(service.llm, "generate", fail)

    response = client.post(
        "/query",
        json={"query": "x"},
        headers={"Authorization": "Bearer dev-hr-manager"},
    )

    assert response.status_code == 503
