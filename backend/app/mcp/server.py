import os
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from app.mcp.tools.notes import (
    create_note_tool,
    delete_note_tool,
    get_note_tool,
    list_notes_tool,
    search_notes_tool,
    update_note_tool,
)

mcp = FastMCP("context-notes")


@mcp.tool()
def list_notes() -> List[Dict[str, Any]]:
    """Return a concise list of the user's notes with metadata only. Use this when the user asks for their notes without full content."""
    return list_notes_tool({})


@mcp.tool()
def search_notes(query: str) -> List[Dict[str, Any]]:
    """Search notes by title, content, or tags. Use this when the user asks about a topic they may have previously written down."""
    return search_notes_tool({"query": query})


@mcp.tool()
def get_note(note_id: str) -> Dict[str, Any]:
    """Retrieve the complete content of a single note by its id."""
    note = get_note_tool({"note_id": note_id})
    if note is None:
        raise ValueError(f"Note {note_id} not found")
    return note


@mcp.tool()
def create_note(title: str, content: str | None = None, tags: List[str] | None = None) -> Dict[str, Any]:
    """Create a new note. Use this for user requests to capture or save information."""
    return create_note_tool({"title": title, "content": content, "tags": tags or []})


@mcp.tool()
def update_note(note_id: str, title: str | None = None, content: str | None = None, tags: List[str] | None = None) -> Dict[str, Any]:
    """Update an existing note. Allows partial updates to title, content, or tags."""
    updated = update_note_tool({"note_id": note_id, "title": title, "content": content, "tags": tags})
    if updated is None:
        raise ValueError(f"Note {note_id} not found")
    return updated


@mcp.tool()
def delete_note(note_id: str) -> Dict[str, Any]:
    """Delete a note permanently."""
    result = delete_note_tool({"note_id": note_id})
    if result.get("deleted") is not True:
        raise ValueError(f"Note {note_id} not found")
    return result


if __name__ == "__main__":
    host = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_SERVER_PORT", "8001"))
    mcp.run(host=host, port=port)
