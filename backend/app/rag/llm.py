from functools import lru_cache

from llama_cpp import Llama

from app.core.config import settings


@lru_cache
def get_llm() -> Llama:
    return Llama(
        model_path=str(settings.model_path),
        n_ctx=settings.llm_context_size,
        verbose=False,
    )


def generate(system_prompt: str, user_prompt: str) -> str:
    response = get_llm().create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=settings.llm_max_tokens,
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"].strip()
