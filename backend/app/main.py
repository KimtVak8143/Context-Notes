from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, notes
from app.db.database import ensure_indexes

app = FastAPI(title="Context Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    ensure_indexes()


app.include_router(notes.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
