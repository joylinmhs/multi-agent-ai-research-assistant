import unittest

from app.agents.fact_checking_agent import FactCheckingAgent
from app.agents.memory_agent import MemoryAgent
from app.agents.summarization_agent import SummarizationAgent


class TestSummarizationAgent(unittest.IsolatedAsyncioTestCase):
    async def test_answers_action_question_with_relevant_sentences(self):
        story = (
            "The Little Sparrow and the Seed Once upon a time, a little sparrow "
            "found a tiny seed on the ground. Instead of eating it, she planted "
            "it near a sunny spot and watered it every day. Days passed. "
            "The sparrow was very happy."
        )

        answer = await SummarizationAgent().summarize(
            [{"text": story, "distance": 0.1}],
            "What did the sparrow do?",
        )

        self.assertEqual(
            answer,
            "A little sparrow found a tiny seed on the ground. Instead of eating it, "
            "she planted it near a sunny spot and watered it every day.",
        )
        self.assertNotIn("Answer to", answer)

    async def test_answers_follow_up_with_next_story_event(self):
        story = (
            "A little sparrow found a tiny seed on the ground. Instead of eating it, "
            "she planted it near a sunny spot and watered it every day. Days passed, "
            "and a small green plant began to grow. The sparrow was very happy."
        )

        answer = await SummarizationAgent().summarize(
            [{"text": story, "distance": 0.1}],
            "What did it do next?",
            previous_answer=(
                "A little sparrow found a tiny seed on the ground. Instead of eating it, "
                "she planted it near a sunny spot and watered it every day."
            ),
        )

        self.assertEqual(answer, "Days passed, and a small green plant began to grow.")


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
