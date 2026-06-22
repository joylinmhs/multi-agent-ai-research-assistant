import uuid
from typing import Any

from app.agents.research_agent import ResearchAgent


class DocumentService:
    def __init__(
        self,
        collection_name: str = "research",
        persist_directory: str | None = None,
        model_name: str = "all-MiniLM-L6-v2",
        embedding_function: Any | None = None,
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.model_name = model_name
        self.embedding_function = embedding_function

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
            embedding_function=self.embedding_function,
        )
        try:
            # Chunk the document into smaller passages to avoid returning whole documents
            def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
                if not text:
                    return []
                chunks: list[str] = []
                start = 0
                length = len(text)
                while start < length:
                    end = min(start + chunk_size, length)
                    chunk = text[start:end]
                    chunks.append(chunk)
                    if end == length:
                        break
                    start = max(0, end - overlap)
                return chunks

            chunks = _chunk_text(content)
            ids: list[str] = []
            docs: list[str] = []
            metas: list[dict[str, Any]] = []
            for idx, chunk in enumerate(chunks):
                cid = f"{document_id}-{idx}"
                ids.append(cid)
                docs.append(chunk)
                m: dict[str, Any] = {k: v for k, v in dict(metadata or {}).items() if v is not None}
                m["parent_document_id"] = document_id
                m["chunk_index"] = idx
                if title is not None:
                    m["title"] = title
                metas.append(m)

            if docs:
                agent.collection.add(documents=docs, metadatas=metas, ids=ids)
        finally:
            agent.close()

        return {
            "document_id": document_id,
            "message": "Document ingested into Chroma successfully",
        }
