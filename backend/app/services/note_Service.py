from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from app.db import database
from app.models.note import Note


def _serialize_note(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc.pop("_id", None)
    return doc


def create_note(title: str, content: Optional[str], tags: Optional[List[str]]):
    note = Note(title=title, content=content, tags=tags or [])
    database.notes_collection.insert_one(note.to_dict())
    return note.to_dict()


def get_note(note_id: UUID | str):
    doc = database.notes_collection.find_one({"id": str(note_id)})
    return _serialize_note(doc)


def list_notes():
    docs = list(database.notes_collection.find().sort("updated_at", -1))
    return [_serialize_note(doc) for doc in docs]


def update_note(note_id: UUID | str, title: Optional[str], content: Optional[str], tags: Optional[List[str]]):
    existing = database.notes_collection.find_one({"id": str(note_id)})
    if not existing:
        return None

    update_data = {"updated_at": datetime.now(timezone.utc).isoformat()}
    if title is not None:
        update_data["title"] = title
    if content is not None:
        update_data["content"] = content
    if tags is not None:
        update_data["tags"] = tags

    database.notes_collection.update_one({"id": str(note_id)}, {"$set": update_data})
    return _serialize_note(database.notes_collection.find_one({"id": str(note_id)}))


def delete_note(note_id: UUID | str):
    result = database.notes_collection.delete_one({"id": str(note_id)})
    return result.deleted_count > 0


def search_notes(q: str):
    regex = {"$regex": q, "$options": "i"}
    docs = list(database.notes_collection.find({
        "$or": [
            {"title": regex},
            {"content": regex},
            {"tags": regex}
        ]
    }).sort("updated_at", -1))
    return [_serialize_note(doc) for doc in docs]
