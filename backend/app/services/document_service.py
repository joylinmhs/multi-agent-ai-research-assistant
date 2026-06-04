import uuid
from typing import Any

from app.agents.research_agent import ResearchAgent


class DocumentService:
    def __init__(
        self,
        collection_name: str = "research",
        persist_directory: str | None = None,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.model_name = model_name

    def ingest_text(
        self,
        content: str,
        document_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        title: str | None = None,
    ) -> dict[str, str]:
        if not content or not content.strip():
            raise ValueError("Document content must not be empty")

        document_id = document_id or str(uuid.uuid4())
        metadata = dict(metadata or {})
        if title:
            metadata["title"] = title

        agent = ResearchAgent(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            model_name=self.model_name,
        )
        try:
            agent.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[document_id],
            )
        finally:
            agent.close()

        return {
            "document_id": document_id,
            "message": "Document ingested into Chroma successfully",
        }
