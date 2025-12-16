# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Meeting Assistant"
    MEDIA_ROOT: str = os.getenv("MEDIA_ROOT", "media")
    AUDIO_FOLDER: str = os.path.join(MEDIA_ROOT, "audio")

    # Limits
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "aac", "ogg"}

settings = Settings()
