import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.config import MONGODB_DB, MONGODB_URI, USE_IN_MEMORY_DB


def _build_client():
    if USE_IN_MEMORY_DB:
        import mongomock

        return mongomock.MongoClient()

    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client
    except (PyMongoError, OSError, ValueError) as exc:
        raise RuntimeError(
            f"MongoDB is not available at {MONGODB_URI}. "
            "Set USE_IN_MEMORY_DB=true only for testing, or start MongoDB locally."
        ) from exc


client = _build_client()
db = client[MONGODB_DB]
notes_collection = db["notes"]


def ensure_indexes():
    notes_collection.create_index([("updated_at", -1)])
    notes_collection.create_index([("title", "text"), ("content", "text"), ("tags", "text")])
