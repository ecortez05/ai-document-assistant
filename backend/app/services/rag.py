from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import TOP_K
from ..models import Chunk, Document
from . import llm

SYSTEM_PROMPT = (
    "You answer questions using only the excerpts provided. "
    "Cite excerpts like [1] or [2] after the claims they support. "
    "If the excerpts don't contain the answer, say you couldn't find it in the documents."
)


def find_chunks(db: Session, user_id: int, question: str, document_id: int | None = None):
    vector = llm.embed([question])[0]
    query = (
        select(Chunk, Document)
        .join(Document, Chunk.document_id == Document.id)
        .where(Document.owner_id == user_id)
        .order_by(Chunk.embedding.cosine_distance(vector))
        .limit(TOP_K)
    )
    if document_id is not None:
        query = query.where(Document.id == document_id)
    return db.execute(query).all()


def build_prompt(question: str, excerpts: list[tuple[str, int, str]]) -> str:
    blocks = [
        f"[{i}] ({name}, page {page})\n{text}"
        for i, (name, page, text) in enumerate(excerpts, start=1)
    ]
    return "Excerpts:\n\n" + "\n\n".join(blocks) + f"\n\nQuestion: {question}"


def answer_question(db: Session, user_id: int, question: str, document_id: int | None = None):
    rows = find_chunks(db, user_id, question, document_id)
    if not rows:
        return "Upload a PDF first, then ask me about it.", []

    excerpts = [(doc.filename, chunk.page, chunk.text) for chunk, doc in rows]
    answer = llm.complete(SYSTEM_PROMPT, build_prompt(question, excerpts))
    sources = [
        {
            "document_id": doc.id,
            "filename": doc.filename,
            "page": chunk.page,
            "snippet": chunk.text[:200],
        }
        for chunk, doc in rows
    ]
    return answer, sources
