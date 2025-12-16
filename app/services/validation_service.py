# app/services/validation_service.py
from fastapi import HTTPException, UploadFile
from app.core.config import settings

def validate_file_extension(file: UploadFile):
    ext = file.filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format: {ext}. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )

def validate_file_size(file: UploadFile):
    size_mb = file.size / (1024 * 1024)
    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size_mb:.2f}MB. Max allowed is {settings.MAX_FILE_SIZE_MB}MB"
        )
