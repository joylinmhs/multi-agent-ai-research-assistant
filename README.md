# Multi-Agent AI Research Assistant using RAG and LLM Agents

A production-style full-stack research assistant that combines multiple AI agents with RAG, embeddings, and modern UI.

## Project Overview

This repository is designed as a resume-worthy capstone project with a clean architecture:

- **Frontend:** React + Tailwind CSS, modern chat UI, dark mode, document management, and agent activity visualization.
- **Backend:** FastAPI, modular routes, async AI pipelines, file upload, embeddings, and vector search.
- **AI Stack:** LangChain + ChromaDB for RAG, with room for CrewAI / LangGraph and open-source LLM support later.
- **Data:** PDF extraction, chunking, semantic retrieval, conversations, and citation tracking.

## Folder Structure

- `backend/` – FastAPI application and AI orchestration.
- `frontend/` – React + Vite application with Tailwind CSS.
- `docs/` – Architecture notes and deployment documentation.

## Initial Setup

1. Install Python dependencies from `backend/requirements.txt`.
2. Install frontend dependencies from `frontend/package.json`.
3. Configure environment variables in `backend/.env`.
4. Run backend with `uvicorn app.main:app --reload`.
5. Run frontend with `npm run dev`.

## Next Steps

- Add PDF upload and extraction.
- Build RAG pipeline and vector store integration.
- Implement multi-agent orchestration.
- Create chat UI and history persistence.
