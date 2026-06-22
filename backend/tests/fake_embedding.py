from typing import Any

from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


class FakeEmbeddingFunction(EmbeddingFunction[Documents]):
    """Small deterministic embedding function for tests with no model downloads."""

    def __init__(self) -> None:
        pass

    def __call__(self, input: Documents) -> Embeddings:
        embeddings: list[list[float]] = []
        for document in input:
            vector = [0.0] * 16
            for token in document.lower().split():
                vector[sum(ord(char) for char in token) % len(vector)] += 1.0
            embeddings.append(vector)
        return embeddings

    @staticmethod
    def name() -> str:
        return "test-fake-embedding"

    @staticmethod
    def build_from_config(config: dict[str, Any]) -> "FakeEmbeddingFunction":
        return FakeEmbeddingFunction()

    def get_config(self) -> dict[str, Any]:
        return {}
