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
      llm.py           wraps the local GGUF model via llama-cpp-python
      chat.py          retrieval + confidence-gating + prompt + generation
    api/
      chat.py          POST /chat endpoint
  scripts/
    ingest.py        rebuilds the FAISS index from data/resume/
  tests/               pytest suite (unit tests, mocked LLM/index by default)
  data/resume/       source documents for the RAG chatbot (markdown + frontmatter)
                     gitignored, personal content, not committed
    about.md
    skills.md
    education.md
    experience/       one file per role
    projects/          one file per project
  data/index/        generated FAISS index, gitignored
  models/             GGUF model file, gitignored
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

### Downloading the model

The GGUF model file is gitignored (too large to commit) and needs to be fetched once per machine:

```
cd backend
.venv\Scripts\python.exe -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='Qwen/Qwen2.5-1.5B-Instruct-GGUF', filename='qwen2.5-1.5b-instruct-q4_k_m.gguf', local_dir='models')"
```

Note: `llama-cpp-python` must be installed from the prebuilt CPU wheel index on Windows, plain `pip install llama-cpp-python` fails building from source due to a MAX_PATH issue in the vendored llama.cpp source tree:

```
pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

## Testing

```
cd backend
.venv\Scripts\python.exe -m pytest -m "not slow"
```

Tests mock the LLM and FAISS index by default, so the suite runs in seconds without needing the model loaded. Tests marked `@pytest.mark.slow` exercise the real local model end-to-end; run them with `pytest -m slow` when you want that extra confidence (they're excluded from the default run and from the pre-push hook).

Add tests for every new feature under `backend/tests/` as the project grows.

### Tests must pass before pushing

This repo has a pre-push git hook (`.githooks/pre-push`) that runs the fast pytest suite and blocks the push if anything fails. It's tracked in git but needs to be pointed to once per clone:

```
git config core.hooksPath .githooks
```

## Status

- [x] Monorepo scaffold (frontend + backend)
- [x] Resume/project content prepped as source documents
- [x] Ingestion pipeline (chunk → embed → FAISS index)
- [x] FastAPI RAG endpoint (`POST /chat`, with retrieval-confidence gating)
- [x] Qwen2.5-1.5B → GGUF conversion + llama-cpp-python wiring
- [x] pytest suite + pre-push test gate
- [ ] Frontend chat UI
- [ ] Railway deployment
