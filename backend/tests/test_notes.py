import os

import mongomock
import pytest
from fastapi.testclient import TestClient

from app import main
from app.db import database


@pytest.fixture(autouse=True)
def mock_mongo():
    database.client = mongomock.MongoClient()
    database.db = database.client["context_test"]
    database.notes_collection = database.db["notes"]
    database.ensure_indexes()
    yield
    database.client.close()


client = TestClient(main.app)


def test_create_get_update_delete_note():
    resp = client.post("/api/v1/notes", json={"title": "Test", "content": "hello", "tags": ["a"]})
    assert resp.status_code == 201
    note = resp.json()
    note_id = note["id"]

    resp = client.get(f"/api/v1/notes/{note_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Test"

    resp = client.get("/api/v1/notes")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.put(f"/api/v1/notes/{note_id}", json={"title": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated"

    resp = client.get("/api/v1/notes/search", params={"q": "Updated"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.delete(f"/api/v1/notes/{note_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/notes/{note_id}")
    assert resp.status_code == 404


def test_validation_error():
    resp = client.post("/api/v1/notes", json={"content": "missing title"})
    assert resp.status_code == 422


def test_not_found_behavior():
    resp = client.get("/api/v1/notes/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
