# Multi-Agent AI Research Assistant using RAG and LLM Agents

A full-stack research assistant that combines a FastAPI API, Chroma retrieval, and focused agents with a React interface.

## Project Overview

The architecture is as follows:
- **Frontend:** React, TypeScript, Vite, and Tailwind CSS.
- **Backend:** FastAPI routes for health checks, document ingestion, uploads, and chat queries.
- **Retrieval:** ChromaDB with Sentence Transformers embeddings and chunk-level citations.
- **Agents:** Retrieval, local summarization, evidence scoring, citations, and bounded in-process session memory.

## Folder Structure
- `backend/` – FastAPI application and AI orchestration.
- `frontend/` – React + Vite application with Tailwind CSS.
- `docs/` – Architecture notes and deployment documentation.

## Initial Setup
1. Create a Python virtual environment and install `backend/requirements.txt`.
2. Copy `backend/.env.example` to `backend/.env` and adjust values as needed.
3. From `backend/`, run `uvicorn app.main:app --reload`.
4. From `frontend/`, run `npm install` and `npm run dev`.

The default embedding model must exist in the local Sentence Transformers cache.
Runtime requests use cached model files so they do not depend on Hugging Face availability.

## Checks
- Backend: `cd backend && python -m unittest discover -s tests -v`
- Frontend: `cd frontend && npm run build`

## Current Limitations
- Answer synthesis is extractive and does not currently call an LLM.
- Confidence is a lexical evidence score, not model-based fact verification.
- Session memory is process-local and is lost when the backend restarts.
- Uploaded PDFs without extractable text are stored but not ingested.
