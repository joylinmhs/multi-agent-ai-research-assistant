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

        # Take top 2 snippets and produce a short synthesized answer.
        # Extract a short context window around query keywords when possible.
        snippets: List[str] = []
        query_terms = []
        if query:
            query_terms = [t.lower() for t in query.split() if len(t) > 2]

        for c in ranked[:2]:
            text = (c.get("text", "") or "").replace("\n", " ")
            snippet = ""
            if query_terms:
                lower = text.lower()
                idx = -1
                for term in query_terms:
                    idx = lower.find(term)
                    if idx >= 0:
                        break
                if idx >= 0:
                    start = max(0, idx - 80)
                    end = min(len(text), idx + 120)
                    snippet = text[start:end].strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(text):
                        snippet = snippet + "..."
            if not snippet:
                # fallback: short prefix
                snippet = (text[:197].rsplit(" ", 1)[0] + "...") if len(text) > 200 else text
            snippets.append(snippet.strip())
        # Basic synthesis: mention query if available
        if query:
            header = f"Answer to: \"{query}\" — "
        else:
            header = "Answer: "

        synthesis = " \n\n ".join(snippets)
        return f"{header}{synthesis}"
