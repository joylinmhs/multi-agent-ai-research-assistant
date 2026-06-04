import os
import sys
import tempfile
import unittest

# Ensure the backend package is importable when running tests from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.document_service import DocumentService
from app.agents.research_agent import ResearchAgent


class TestDocumentService(unittest.IsolatedAsyncioTestCase):
    async def test_ingest_text_and_retrieve(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            ingest_service = DocumentService(persist_directory=temp_dir)
            response = ingest_service.ingest_text(
                content="This document should be searchable by Chroma.",
                title="Test Document",
                metadata={"source": "unit-test"},
            )

            self.assertIn("document_id", response)
            self.assertEqual(response["message"], "Document ingested into Chroma successfully")

            agent = ResearchAgent(persist_directory=temp_dir)
            try:
                results = await agent.retrieve("searchable by Chroma")
            finally:
                agent.close()

            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)
            self.assertIn("text", results[0])
            self.assertIn("Chroma", results[0]["text"])
            self.assertEqual(results[0]["metadata"].get("source"), "unit-test")


if __name__ == "__main__":
    unittest.main()
