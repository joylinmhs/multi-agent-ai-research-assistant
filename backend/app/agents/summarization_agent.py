from typing import List, Optional

class SummarizationAgent:
    """Summarization Agent converts retrieved chunks into concise answers.

    This is a simple local synthesizer: it selects the most relevant chunks
    (by `distance`) and returns a short synthesized answer rather than
    concatenating full documents. In future this should call an LLM.
    """

    async def summarize(self, chunks: List[dict], query: Optional[str] = None) -> str:
        if not chunks:
            return "I couldn't find relevant documents to answer that question."

        # Prefer chunks with smallest distance (most relevant)
        ranked = sorted(chunks, key=lambda c: (c.get("distance") is None, c.get("distance")))

        # Take top 2 snippets and produce a short synthesized answer
        snippets: List[str] = []
        for c in ranked[:2]:
            text = c.get("text", "") or ""
            # shorten long texts to a short excerpt
            excerpt = text.replace("\n", " ")
            if len(excerpt) > 500:
                excerpt = excerpt[:497].rsplit(" ", 1)[0] + "..."
            snippets.append(excerpt.strip())

        # Basic synthesis: mention query if available
        if query:
            header = f"Answer to: \"{query}\" — "
        else:
            header = "Answer: "

        synthesis = " \n\n ".join(snippets)
        return f"{header}{synthesis}"
