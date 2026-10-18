from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..auth import current_user
from ..config import MAX_UPLOAD_MB
from ..db import get_db
from ..models import Chunk, Document, User
from ..schemas import DocumentOut
from ..services import llm
from ..services.pdf import extract_chunks

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentOut])
def list_documents(user: User = Depends(current_user), db: Session = Depends(get_db)):
    query = select(Document).where(Document.owner_id == user.id).order_by(Document.created_at.desc())
    return db.scalars(query).all()


@router.post("", response_model=DocumentOut, status_code=201)
async def upload(file: UploadFile, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    data = await file.read()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"File is larger than {MAX_UPLOAD_MB}MB")

    try:
        page_count, pieces = extract_chunks(data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if not pieces:
        raise HTTPException(422, "No text found in that PDF (is it a scan?)")

    vectors = llm.embed([text for _, text in pieces])

    doc = Document(owner_id=user.id, filename=file.filename, page_count=page_count)
    db.add(doc)
    db.flush()
    db.add_all(
        Chunk(document_id=doc.id, page=page, text=text, embedding=vec)
        for (page, text), vec in zip(pieces, vectors)
    )
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{doc_id}", status_code=204)
def delete_document(doc_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    doc = db.get(Document, doc_id)
    if not doc or doc.owner_id != user.id:
        raise HTTPException(404, "Document not found")
    db.delete(doc)
    db.commit()
