# portfolio

Personal portfolio/resume site with a built-in RAG chatbot that answers questions about my work, and only my work.

## Stack

- **Frontend:** React + TypeScript, built/run with Bun (Vite)
- **Backend:** FastAPI (Python)
- **Chatbot:** self-hosted, no paid APIs
  - Generation: Qwen2.5-1.5B-Instruct, quantized to GGUF, run via `llama-cpp-python`
  - Embeddings: `sentence-transformers` (`all-MiniLM-L6-v2`)
  - Vector index: FAISS
  - Orchestration: LangChain
  - Scope guardrail: system prompt + retrieval-confidence gating (off-topic questions are refused before reaching the model)
- **Hosting:** Railway

## Project structure

```
frontend/   React + TS app (Bun/Vite)
backend/    FastAPI app
  app/
    main.py          FastAPI entrypoint, CORS
    core/config.py   settings (pydantic-settings)
    rag/
      documents.py   loads + chunks the resume markdown source docs
      index.py        builds/loads the FAISS index (MiniLM embeddings)
  scripts/
    ingest.py        rebuilds the FAISS index from data/resume/
  data/resume/       source documents for the RAG chatbot (markdown + frontmatter)
                     gitignored, personal content, not committed
    about.md
    skills.md
    education.md
    experience/       one file per role
    projects/          one file per project
  data/index/        generated FAISS index, gitignored
```

## Running locally

### Backend

```
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```
cd frontend
bun dev
```

### Rebuilding the RAG index

Run after adding/editing anything under `backend/data/resume/`:

```
cd backend
.venv\Scripts\python.exe scripts\ingest.py
```

## Status

- [x] Monorepo scaffold (frontend + backend)
- [x] Resume/project content prepped as source documents
- [x] Ingestion pipeline (chunk → embed → FAISS index)
- [ ] FastAPI RAG endpoint
- [ ] Qwen2.5-1.5B → GGUF conversion + llama-cpp-python wiring
- [ ] Railway deployment
