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
            meta = c.get("metadata") or {}
            doc_id = meta.get("parent_document_id") or c.get("document_id") or "unknown"
            page = meta.get("page", 0)
            text = (c.get("text", "") or "")
            dist = c.get("distance")
            try:
                confidence = max(0.0, 1.0 - float(dist)) if dist is not None else 0.0
            except Exception:
                confidence = 0.0
            sources.append(
                SourceReference(
                    document_id=doc_id,
                    page_number=page,
                    snippet=text[:200],
                    confidence=confidence,
                )
            )
        return sources
