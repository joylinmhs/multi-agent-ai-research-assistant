import uuid
from pathlib import Path
from fastapi import UploadFile
import pdfplumber

from app.core.config import settings
from app.services.document_service import DocumentService


class FileService:
    def __init__(self):
        self.storage_dir = Path(settings.CHROMA_DB_DIR).parent / "uploads"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def save_document(self, file: UploadFile) -> dict:
        filename = f"{uuid.uuid4()}_{file.filename}"
        destination = self.storage_dir / filename

        contents = await file.read()
        with destination.open("wb") as buffer:
            buffer.write(contents)

        document_id = str(uuid.uuid4())
        text = self._extract_text(file.content_type, destination, contents)
        ingested = False

        if text and text.strip():
            DocumentService().ingest_text(
                content=text,
                document_id=document_id,
                metadata={"filename": file.filename},
            )
            ingested = True
            message = "File uploaded and ingested into Chroma successfully"
        else:
            message = "File uploaded successfully"

        return {
            "filename": filename,
            "message": message,
            "document_id": document_id,
            "ingested": ingested,
        }

    def _extract_text(self, content_type: str, path: Path, contents: bytes) -> str | None:
        if content_type == "text/plain":
            return contents.decode("utf-8", errors="replace")

        if content_type == "application/pdf":
            try:
                with pdfplumber.open(path) as pdf:
                    return "\n\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    ).strip()
            except Exception:
                return None

        return None
