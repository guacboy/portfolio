from dataclasses import dataclass, field
from functools import lru_cache

from app.core.config import settings
from app.rag.index import load_index
from app.rag.llm import generate

REFUSAL = "I can only answer questions about Dylan's work and resume."

SYSTEM_PROMPT = (
    "You are an assistant on Dylan Pham Nguyen's portfolio website. "
    "You answer questions ONLY about Dylan's work experience, projects, skills, and education, "
    "using ONLY the context provided below the question. "
    "If the question is not about Dylan's work or resume, or the context doesn't contain the answer, "
    f'respond with exactly: "{REFUSAL}" '
    "Do not use any knowledge beyond the given context."
)


@dataclass
class ChatResult:
    answer: str
    sources: list[str] = field(default_factory=list)


@lru_cache
def _get_index():
    return load_index()


def answer(query: str) -> ChatResult:
    index = _get_index()
    results = index.similarity_search_with_score(query, k=settings.retrieval_top_k)

    if not results or results[0][1] > settings.retrieval_distance_threshold:
        return ChatResult(answer=REFUSAL)

    context = "\n\n".join(doc.page_content for doc, _ in results)
    sources = sorted({doc.metadata.get("source", "") for doc, _ in results})

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"
    reply = generate(SYSTEM_PROMPT, user_prompt)
    return ChatResult(answer=reply, sources=sources)
