import os
import sys
import tempfile
import unittest

# Ensure the backend package is importable when running tests from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.research_agent import ResearchAgent


class TestResearchAgent(unittest.IsolatedAsyncioTestCase):
    async def test_retrieve_with_chroma_index(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            agent = ResearchAgent(collection_name="test_research_agent", persist_directory=temp_dir)
            try:
                agent.collection.add(
                    documents=["This is a Chroma retrieval test document."],
                    metadatas=[{"source": "unit-test"}],
                    ids=["test-doc-1"],
                )

                res = await agent.retrieve("retrieval test")
            finally:
                agent.close()

            self.assertIsInstance(res, list)
            self.assertGreater(len(res), 0)
            self.assertIn("text", res[0])
            self.assertIn("Chroma retrieval test document", res[0]["text"])
            self.assertEqual(res[0]["metadata"].get("source"), "unit-test")

    async def test_empty_query(self):
        agent = ResearchAgent()
        res = await agent.retrieve("")
        self.assertEqual(res, [])


if __name__ == "__main__":
    unittest.main()
