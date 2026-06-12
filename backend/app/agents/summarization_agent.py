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

        # Take the single most relevant chunk and produce a short answer.
        top = ranked[0]
        text = (top.get("text", "") or "").replace("\n", " ")
        query_terms = [t.lower() for t in query.split() if len(t) > 2] if query else []

        snippet = ""
        if query_terms:
            lower = text.lower()
            idx = -1
            for term in query_terms:
                idx = lower.find(term)
                if idx >= 0:
                    break
            if idx >= 0:
                start = max(0, idx - 60)
                end = min(len(text), idx + 90)
                snippet = text[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(text):
                    snippet = snippet + "..."

        if not snippet:
            snippet = (text[:150].rsplit(" ", 1)[0] + "...") if len(text) > 160 else text

        header = f"Answer to: \"{query}\" — " if query else "Answer: "
        return f"{header}{snippet.strip()}"
