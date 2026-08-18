from fastapi import APIRouter
from pydantic import BaseModel

from app.services import chat_service

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_notes(payload: ChatRequest):
    reply = chat_service.generate_reply(payload.message)
    return {"reply": reply}
from fastapi import APIRouter
from pydantic import BaseModel

from app.services import chat_service

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_notes(payload: ChatRequest):
    reply = chat_service.generate_reply(payload.message)
    return {"reply": reply}
