import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from starlette.datastructures import UploadFile

# Ensure the backend package is importable when running tests from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.file_service import FileService


class TestFileService(unittest.IsolatedAsyncioTestCase):
    async def test_save_document_uploads_and_ingests_text_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = FileService()
            service.storage_dir = Path(temp_dir)

            upload_file = UploadFile(io.BytesIO(b"Hello Chroma ingestion"), filename="test.txt")
            upload_file.content_type = "text/plain"

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


if __name__ == "__main__":
    unittest.main()
