from openai import OpenAI

from ..config import CHAT_MODEL, EMBED_MODEL, OPENAI_API_KEY

_client = None


def client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def embed(texts: list[str]) -> list[list[float]]:
    vectors = []
    # the API caps how many inputs we can send at once
    for i in range(0, len(texts), 100):
        resp = client().embeddings.create(model=EMBED_MODEL, input=texts[i : i + 100])
        vectors.extend(d.embedding for d in resp.data)
    return vectors


def complete(system: str, user: str) -> str:
    resp = client().chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content or ""
