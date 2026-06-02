from typing import List
from app.schemas.chat import SourceReference

class CitationAgent:
    """Citation Agent attaches source references to each response."""

    async def generate_sources(self, chunks: List[dict]) -> List[SourceReference]:
        # TODO: map chunk metadata to structured citation references.
        return [
            SourceReference(
                document_id=chunks[0].get("document_id", "unknown"),
                page_number=chunks[0].get("metadata", {}).get("page", 0),
                snippet=chunks[0].get("text", ""),
                confidence=0.9,
            )
        ]
