from fastapi import APIRouter
from app.questions.service import get_total_questions_count

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/count")
def get_count():
    """Internal route to check total seeded questions."""
    count = get_total_questions_count()
    return {"total_questions": count}
