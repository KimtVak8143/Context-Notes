from __future__ import annotations

from typing import Any, Dict, List, Optional

from app import services


def _note_summary(note: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": note.get("id"),
        "title": note.get("title"),
        "tags": note.get("tags", []),
        "updated_at": note.get("updated_at"),
    }


def list_notes_tool(_: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Return a concise list of the user's note metadata."""
    notes = services.note_service.list_notes()
    return [_note_summary(note) for note in notes]


def search_notes_tool(payload: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Search notes by title, content, or tags. Use this when the user asks what they wrote about a topic."""
    query = (payload or {}).get("query", "")
    if not query:
        return []

    results = services.note_service.search_notes(query)
    return [
        {
            "id": note.get("id"),
            "title": note.get("title"),
            "snippet": (note.get("content") or "")[:180],
            "tags": note.get("tags", []),
        }
        for note in results
    ]


def get_note_tool(payload: Dict[str, Any] | None = None) -> Optional[Dict[str, Any]]:
    """Retrieve the full contents of a note by id."""
    note_id = (payload or {}).get("note_id")
    if not note_id:
        return None

    return services.note_service.get_note(note_id)


def create_note_tool(payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Create a new note with a title, content, and optional tags. Use this when the user asks to save new information."""
    data = payload or {}
    title = data.get("title")
    if not title:
        raise ValueError("A note title is required.")

    return services.note_service.create_note(
        title=title,
        content=data.get("content"),
        tags=data.get("tags", []),
    )


def update_note_tool(payload: Dict[str, Any] | None = None) -> Optional[Dict[str, Any]]:
    """Update an existing note. Allows title, content, and tags to be changed as needed."""
    data = payload or {}
    note_id = data.get("note_id")
    if not note_id:
        raise ValueError("A note_id is required.")

    return services.note_service.update_note(
        note_id=note_id,
        title=data.get("title"),
        content=data.get("content"),
        tags=data.get("tags"),
    )


def delete_note_tool(payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Delete a note permanently."""
    note_id = (payload or {}).get("note_id")
    if not note_id:
        raise ValueError("A note_id is required.")

    deleted = services.note_service.delete_note(note_id)
    return {"deleted": deleted}
