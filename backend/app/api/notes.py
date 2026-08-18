from fastapi import APIRouter, HTTPException, Query, status
from typing import List
from uuid import UUID

from app.schemas.note import NoteCreate, NoteOut, NoteUpdate
from app import services

router = APIRouter()


@router.get("/notes", response_model=List[NoteOut])
def notes_list():
    return services.note_service.list_notes()


@router.get("/notes/search")
def notes_search(q: str = Query(...)):
    return services.note_service.search_notes(q)


@router.get("/notes/{note_id}", response_model=NoteOut)
def notes_get(note_id: UUID):
    note = services.note_service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOTE_NOT_FOUND", "message": "The requested note does not exist."}})
    return note


@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def notes_create(payload: NoteCreate):
    return services.note_service.create_note(payload.title, payload.content, payload.tags)


@router.put("/notes/{note_id}", response_model=NoteOut)
def notes_update(note_id: UUID, payload: NoteUpdate):
    updated = services.note_service.update_note(note_id, payload.title, payload.content, payload.tags)
    if not updated:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOTE_NOT_FOUND", "message": "The requested note does not exist."}})
    return updated


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def notes_delete(note_id: UUID):
    deleted = services.note_service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOTE_NOT_FOUND", "message": "The requested note does not exist."}})
    return None
