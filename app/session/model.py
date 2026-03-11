from pydantic import BaseModel, Field
from typing import List

class AnswerHistory(BaseModel):
    question_id: str
    difficulty: float
    topic: str
    selected_answer: str
    correct: bool
    timestamp: str

class Session(BaseModel):
    session_id: str = Field(alias="_id")
    ability_score: float
    questions_answered: int = 0
    history: List[AnswerHistory] = []
    completed: bool = False
    created_at: str

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str
