import os
import sys
import unittest

# Ensure the backend package is importable when running tests from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.research_agent import ResearchAgent


class TestResearchAgent(unittest.IsolatedAsyncioTestCase):
    async def test_retrieve_placeholder(self):
        agent = ResearchAgent()
        res = await agent.retrieve("test query")
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)
        self.assertIn("text", res[0])

    async def test_empty_query(self):
        agent = ResearchAgent()
        res = await agent.retrieve("")
        self.assertEqual(res, [])


if __name__ == "__main__":
    unittest.main()
