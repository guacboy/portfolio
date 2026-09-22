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

## Status

- [x] Monorepo scaffold (frontend + backend)
- [ ] Resume/project content prepped as source documents
- [ ] Ingestion pipeline (chunk → embed → FAISS index)
- [ ] FastAPI RAG endpoint
- [ ] Qwen2.5-1.5B → GGUF conversion + llama-cpp-python wiring
- [ ] Railway deployment
