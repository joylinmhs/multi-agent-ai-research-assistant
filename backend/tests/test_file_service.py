import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Ensure the backend package is importable when running tests from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.file_service import FileService


class TestFileService(unittest.IsolatedAsyncioTestCase):
    async def test_save_document_uploads_and_ingests_text_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = FileService()
            service.storage_dir = Path(temp_dir)

            class DummyUploadFile:
                def __init__(self, filename: str, content_type: str, data: bytes):
                    self.filename = filename
                    self.content_type = content_type
                    self._buffer = io.BytesIO(data)

                async def read(self, size: int = -1):
                    self._buffer.seek(0)
                    return self._buffer.read(size)

            upload_file = DummyUploadFile(
                filename="test.txt",
                content_type="text/plain",
                data=b"Hello Chroma ingestion",
            )

            with patch("app.services.file_service.DocumentService") as MockDocumentService:
                mock_instance = MockDocumentService.return_value
                mock_instance.ingest_text.return_value = {
                    "document_id": "test-doc-id",
                    "message": "Document ingested into Chroma successfully",
                }

                response = await service.save_document(upload_file)

                mock_instance.ingest_text.assert_called_once()
                self.assertTrue(response["ingested"])
                self.assertEqual(response["message"], "File uploaded and ingested into Chroma successfully")
                self.assertTrue((Path(temp_dir) / response["filename"]).exists())

    async def test_save_document_sanitizes_filename(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = FileService()
            service.storage_dir = Path(temp_dir)

            class DummyUploadFile:
                filename = "../unsafe.txt"
                content_type = "text/plain"

                async def read(self, size: int = -1):
                    return b"safe content"

            with patch("app.services.file_service.DocumentService"):
                response = await service.save_document(DummyUploadFile())

            self.assertNotIn("..", response["filename"])
            self.assertEqual(Path(response["filename"]).parent, Path("."))
            self.assertTrue((Path(temp_dir) / response["filename"]).exists())

    async def test_save_document_rejects_oversized_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = FileService()
            service.storage_dir = Path(temp_dir)

            class DummyUploadFile:
                filename = "large.txt"
                content_type = "text/plain"

                async def read(self, size: int = -1):
                    return b"x" * size

            with self.assertRaisesRegex(ValueError, "upload limit"):
                await service.save_document(DummyUploadFile())

            self.assertEqual(list(Path(temp_dir).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
