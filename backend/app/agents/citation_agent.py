from typing import List
from app.schemas.chat import SourceReference

class CitationAgent:
    """Citation Agent attaches source references to each response."""

    async def generate_sources(self, chunks: List[dict]) -> List[SourceReference]:
        # Map top relevant chunks into SourceReference objects.
        if not chunks:
            return []

        ranked = sorted(chunks, key=lambda c: (c.get("distance") is None, c.get("distance")))
        sources: List[SourceReference] = []
        for c in ranked[:3]:
            sources.append(
                SourceReference(
                    document_id=c.get("document_id", "unknown"),
                    page_number=c.get("metadata", {}).get("page", 0),
                    snippet=(c.get("text", "") or "")[:500],
                    confidence=0.9,
                )
            )
        return sources
