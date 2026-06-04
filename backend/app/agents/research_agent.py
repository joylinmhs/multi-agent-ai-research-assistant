import asyncio
import logging
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions

from app.core.config import settings

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Research Agent handles semantic retrieval and relevant chunk selection."""

    def __init__(
        self,
        collection_name: str = "research",
        persist_directory: str | None = None,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory or settings.CHROMA_DB_DIR)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.Client(
            settings=ChromaSettings(
                is_persistent=True,
                persist_directory=str(self.persist_directory),
            )
        )
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
        )

    async def retrieve(self, query: str, context: dict | None = None, n_results: int = 5) -> list[dict[str, Any]]:
        """Retrieve relevant document chunks for a query."""
        if not query or not query.strip():
            logger.warning("ResearchAgent.retrieve called with empty query")
            return []

        logger.debug(
            "ResearchAgent.retrieve called",
            extra={"query": query, "context_keys": list(context.keys()) if context else []},
        )

        return await asyncio.to_thread(self._query_collection, query, n_results)

    def _query_collection(self, query: str, n_results: int) -> list[dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "ids", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]

        chunks: list[dict[str, Any]] = []
        for idx, document_text in enumerate(documents):
            chunks.append(
                {
                    "document_id": ids[idx] if idx < len(ids) else f"chunk-{idx}",
                    "text": document_text,
                    "metadata": metadatas[idx] if idx < len(metadatas) else {},
                    "distance": distances[idx] if idx < len(distances) else None,
                }
            )
        return chunks
