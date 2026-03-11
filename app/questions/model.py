from pydantic import BaseModel, Field
from typing import List

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    difficulty: float = Field(ge=0.1, le=1.0)
    topic: str
    tags: List[str] = []

class QuestionResponse(QuestionBase):
    id: str

class QuestionDB(QuestionBase):
    id: str = Field(alias="_id")
    correct_answer: str

