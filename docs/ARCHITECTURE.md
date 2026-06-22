# Architecture Overview

## Core Layers

- **API Layer** (`backend/app/api`) - FastAPI routes and versioned endpoints.
- **Agent Layer** (`backend/app/agents`) - Retrieval, extractive summarization, evidence scoring, citations, and process-local memory.
- **Service Layer** (`backend/app/services`) - File handling, text chunking, Chroma ingestion, and chat orchestration.
- **Vector Store** - Persistent Chroma collections using Sentence Transformers embeddings.
- **Database Layer** (`backend/app/db`) - SQLAlchemy scaffolding; it is not yet used by the request flow.
- **Schema Layer** (`backend/app/schemas`) - Pydantic request and response models.

## Data Flow

1. The user uploads a PDF or text file, or submits text directly.
2. The backend extracts and chunks the text.
3. Embeddings are stored in Chroma.
4. The user sends a query to the chat endpoint.
5. Research Agent retrieves relevant chunks with semantic search.
6. Summarization Agent extracts a concise answer from the top result.
7. Fact-Checking Agent calculates lexical overlap with retrieved evidence.
8. Citation Agent attaches source snippets and confidence values.
9. Memory Agent retains bounded conversation context for the life of the backend process.
