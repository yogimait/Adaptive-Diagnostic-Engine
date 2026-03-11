from fastapi import APIRouter
from app.session.service import start_new_session, process_answer
from app.session.model import SubmitAnswerRequest
from app.ai_insights.study_plan_generator import get_session_result_and_plan

router = APIRouter(tags=["Session"])

@router.post("/start-session")
def start_session():
    return start_new_session()

@router.post("/submit-answer")
def submit_answer(payload: SubmitAnswerRequest):
    return process_answer(
        session_id=payload.session_id,
        question_id=payload.question_id,
        answer=payload.answer
    )

@router.get("/result/{session_id}")
def get_result(session_id: str):
    return get_session_result_and_plan(session_id)
