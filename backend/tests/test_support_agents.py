import unittest

from app.agents.fact_checking_agent import FactCheckingAgent
from app.agents.memory_agent import MemoryAgent


class TestFactCheckingAgent(unittest.IsolatedAsyncioTestCase):
    async def test_confidence_uses_available_evidence(self):
        agent = FactCheckingAgent()
        result = await agent.verify(
            "Apples are always blue",
            [{"text": "Most ripe apples are red or green."}],
        )

        self.assertGreater(result["confidence"], 0.0)
        self.assertLess(result["confidence"], 1.0)

    async def test_confidence_is_zero_without_evidence(self):
        result = await FactCheckingAgent().verify("Unsupported answer", [])
        self.assertEqual(result["confidence"], 0.0)


class TestMemoryAgent(unittest.IsolatedAsyncioTestCase):
    async def test_context_is_stored_by_session_and_bounded(self):
        agent = MemoryAgent(max_messages_per_session=2)
        await agent.save_context("one", "first", "answer one")
        await agent.save_context("one", "second", "answer two")

        context = await agent.load_context("one")
        other_context = await agent.load_context("two")

        self.assertEqual(len(context["history"]), 2)
        self.assertEqual(context["history"][0]["content"], "second")
        self.assertEqual(other_context["history"], [])


if __name__ == "__main__":
    unittest.main()
