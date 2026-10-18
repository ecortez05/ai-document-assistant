from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import current_user
from ..db import get_db
from ..models import User
from ..schemas import Answer, Question
from ..services.rag import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=Answer)
def ask(body: Question, user: User = Depends(current_user), db: Session = Depends(get_db)):
    answer, sources = answer_question(db, user.id, body.question, body.document_id)
    return Answer(answer=answer, sources=sources)
