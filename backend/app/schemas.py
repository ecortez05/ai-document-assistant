from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DocumentOut(BaseModel):
    id: int
    filename: str
    page_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class Question(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    document_id: int | None = None


class Source(BaseModel):
    document_id: int
    filename: str
    page: int
    snippet: str


class Answer(BaseModel):
    answer: str
    sources: list[Source]
