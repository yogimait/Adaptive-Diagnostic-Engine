from typing import List
from app.questions.repository import count_questions, get_random_question_near_difficulty
from app.questions.model import QuestionResponse
from app.core.errors import QuestionNotFound

def get_total_questions_count() -> int:
    return count_questions()

def select_next_question(ability: float, asked_questions: List[str]) -> QuestionResponse:
    question_db = get_random_question_near_difficulty(ability, asked_questions)
    if not question_db:
        raise QuestionNotFound("No more questions available to serve.")
        
    # Excludes correct_answer by parsing into QuestionResponse representation
    return QuestionResponse(
        id=question_db.id,
        question=question_db.question,
        options=question_db.options,
        difficulty=question_db.difficulty,
        topic=question_db.topic,
        tags=question_db.tags
    )
