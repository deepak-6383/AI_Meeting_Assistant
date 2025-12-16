# app/schemas/audio.py
from pydantic import BaseModel
from uuid import UUID

class UploadResponse(BaseModel):
    batch_id: UUID
    files_received: int
    status: str
    next_step: str
