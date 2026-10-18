from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..auth import check_password, hash_password, make_token
from ..db import get_db
from ..models import User
from ..schemas import Credentials, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
def register(body: Credentials, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(409, "That email is already registered")
    user = User(email=email, password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    return Token(access_token=make_token(user.id))


@router.post("/login", response_model=Token)
def login(body: Credentials, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if not user or not check_password(body.password, user.password_hash):
        raise HTTPException(401, "Wrong email or password")
    return Token(access_token=make_token(user.id))
