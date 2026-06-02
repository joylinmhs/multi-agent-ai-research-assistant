from typing import List

class SummarizationAgent:
    """Summarization Agent converts retrieved chunks into user-facing summaries."""

    async def summarize(self, chunks: List[dict]) -> str:
        # TODO: call an LLM chain to create concise and detailed summaries.
        snippet_text = " ".join(chunk.get("text", "") for chunk in chunks)
        return f"Summarized answer based on retrieved content: {snippet_text}"
