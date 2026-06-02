# Architecture Overview

## Core Layers

- **API Layer** (`backend/app/api`) — FastAPI routes and versioned endpoints.
- **Agent Layer** (`backend/app/agents`) — Separate agent classes for research, summarization, fact-checking, citation, and memory.
- **Service Layer** (`backend/app/services`) — Business logic for embeddings, file ingestion, and session management.
- **RAG Layer** (`backend/app/rag`) — Retrieval augmented generation pipeline and vector store helpers.
- **Database Layer** (`backend/app/db`) — Persistence for chat sessions, metadata, and user documents.
- **Schema Layer** (`backend/app/schemas`) — Pydantic request/response models.

## Data Flow

1. User uploads files via frontend.
2. Backend extracts text and chunk metadata.
3. Embeddings are generated and stored in Chroma.
4. User sends query to chat endpoint.
5. Research Agent retrieves relevant documents via semantic search.
6. Summarization Agent drafts the answer.
7. Fact-Checking Agent verifies claims and attaches confidence.
8. Citation Agent returns sources and references.
9. Memory Agent logs conversation context for later use.
