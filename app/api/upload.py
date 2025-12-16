# app/api/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.db.models import AudioFile, Batch
from app.schemas.audio import UploadResponse
from app.services.validation_service import validate_file_extension, validate_file_size
from app.services.storage_service import save_audio_file
from app.workers.tasks import enqueue_transcription

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-audio", response_model=UploadResponse)
def upload_audio(
    files: List[UploadFile] = File(...),
    user_id: str = "demo_user",
    db=Depends(get_db)
):

    if len(files) < 2 or len(files) > 5:
        raise HTTPException(400, "Upload between 2 to 5 audio files")

    batch = Batch()
    db.add(batch)
    db.commit()
    db.refresh(batch)

    for f in files:
        validate_file_extension(f)
        validate_file_size(f)

        new_name, file_path = save_audio_file(f, user_id)

        audio_record = AudioFile(
            batch_id=batch.id,
            filename=new_name,
            filepath=file_path,
            file_size_mb=f.size / (1024 * 1024),
            cleanup_at=datetime.utcnow() + timedelta(days=7)
        )

        db.add(audio_record)
        db.commit()
        db.refresh(audio_record)

        enqueue_transcription(str(audio_record.id))

    return UploadResponse(
        batch_id=batch.id,
        files_received=len(files),
        status="uploaded",
        next_step="transcription will begin in Phase‑2"
    )
