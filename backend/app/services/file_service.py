import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

class FileService:
    def __init__(self):
        self.storage_dir = Path(settings.CHROMA_DB_DIR).parent / "uploads"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def save_document(self, file: UploadFile) -> dict:
        filename = f"{uuid.uuid4()}_{file.filename}"
        destination = self.storage_dir / filename

        with destination.open("wb") as buffer:
            contents = await file.read()
            buffer.write(contents)

        return {
            "filename": filename,
            "message": "File uploaded successfully",
            "document_id": str(uuid.uuid4()),
        }
