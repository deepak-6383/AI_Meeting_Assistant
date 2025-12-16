# app/services/storage_service.py
import os
import uuid
from datetime import datetime
from app.core.config import settings

def save_audio_file(file, user_id):
    today = datetime.now()
    folder_path = os.path.join(
        settings.AUDIO_FOLDER,
        str(user_id),
        str(today.year),
        str(today.month),
        str(today.day)
    )
    
    os.makedirs(folder_path, exist_ok=True)

    ext = file.filename.split(".")[-1].lower()
    new_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(folder_path, new_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return new_name, file_path
