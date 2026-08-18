import mongomock
import pytest

from app.db import database
from app.mcp.tools.notes import (
    create_note_tool,
    delete_note_tool,
    get_note_tool,
    list_notes_tool,
    search_notes_tool,
    update_note_tool,
)


@pytest.fixture(autouse=True)
def mock_mongo():
    database.client = mongomock.MongoClient()
    database.db = database.client["context_test"]
    database.notes_collection = database.db["notes"]
    database.ensure_indexes()
    yield
    database.client.close()


def test_list_notes_tool_returns_metadata():
    create_note_tool({"title": "Alpha", "content": "One", "tags": ["work"]})
    create_note_tool({"title": "Beta", "content": "Two", "tags": ["personal"]})

    notes = list_notes_tool({})

    assert len(notes) == 2
    assert all({"id", "title", "tags", "updated_at"}.issubset(note) for note in notes)
    assert notes[0]["title"] in {"Alpha", "Beta"}


def test_search_notes_tool_filters_results():
    create_note_tool({"title": "Kubernetes Networking", "content": "CNI and ingress", "tags": ["kubernetes"]})

    results = search_notes_tool({"query": "kubernetes"})

    assert len(results) == 1
    assert results[0]["title"] == "Kubernetes Networking"
    assert "kubernetes" in results[0]["tags"]


def test_get_note_tool_returns_full_content():
    created = create_note_tool({"title": "K8s", "content": "NodePort", "tags": ["ops"]})
    loaded = get_note_tool({"note_id": created["id"]})

    assert loaded["title"] == "K8s"
    assert loaded["content"] == "NodePort"


def test_update_note_tool_updates_selected_note():
    created = create_note_tool({"title": "Old", "content": "Before", "tags": ["a"]})

    updated = update_note_tool({"note_id": created["id"], "title": "New", "content": "After"})

    assert updated["title"] == "New"
    assert updated["content"] == "After"


def test_delete_note_tool_removes_note():
    created = create_note_tool({"title": "Remove me", "content": "Delete", "tags": ["tmp"]})

    result = delete_note_tool({"note_id": created["id"]})

    assert result["deleted"] is True
    assert get_note_tool({"note_id": created["id"]}) is None
