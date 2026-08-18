from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class NoteOut(NoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Handle pydantic v1 vs v2 differences at class definition time
try:
    # pydantic v2 exposes __version__ as a string
    import pydantic as _pyd
    _major = int(_pyd.__version__.split(".")[0])
except Exception:
    _major = 1

if _major >= 2:
    # pydantic v2
    class NoteOut(NoteBase):
        id: UUID
        created_at: datetime
        updated_at: datetime

        model_config = {"from_attributes": True}
else:
    # pydantic v1
    class NoteOut(NoteBase):
        id: UUID
        created_at: datetime
        updated_at: datetime

        class Config:
            orm_mode = True
