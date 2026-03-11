import logging
from app.session.model import Session, AnswerHistory
from app.session.repository import create_session, get_session, update_session
from app.questions.repository import get_question_by_id
from app.questions.service import select_next_question
from app.adaptive_engine.ability_calculator import calculate_new_ability
from app.core.errors import SessionNotFound, QuestionNotFound, TestCompletedError, ResultNotReadyError, InvalidAnswerError
from app.core.utils import generate_session_id, current_timestamp
from app.config import ABILITY_START, TEST_LENGTH

logger = logging.getLogger(__name__)

def start_new_session():
    session_id = generate_session_id()
    new_session = Session(
        _id=session_id,
        ability_score=ABILITY_START,
        created_at=current_timestamp()
    )
    create_session(new_session)
    logger.info(f"Session started: {session_id}")
    
    # Serve first question
    next_question = select_next_question(new_session.ability_score, [])
    logger.info(f"Question served to {session_id} - Difficulty: {next_question.difficulty}")
    
    return {
        "session_id": session_id,
        "question_id": next_question.id,
        "question": next_question.question,
        "options": next_question.options,
        "difficulty": next_question.difficulty
    }

def process_answer(session_id: str, question_id: str, answer: str):
    session = get_session(session_id)
    if not session:
        raise SessionNotFound()
        
    if session.completed:
        raise TestCompletedError()
        
    question = get_question_by_id(question_id)
    if not question:
        raise QuestionNotFound()
        
    if answer not in question.options:
        raise InvalidAnswerError()
        
    is_correct = (answer == question.correct_answer)
    
    # Update ability
    old_ability = session.ability_score
    session.ability_score = calculate_new_ability(session.ability_score, is_correct)
    logger.info(f"Session {session_id} ability updated: {old_ability} -> {session.ability_score}")
    
    # Append history
    history_entry = AnswerHistory(
        question_id=question_id,
        difficulty=question.difficulty,
        topic=question.topic,
        selected_answer=answer,
        correct=is_correct,
        timestamp=current_timestamp()
    )
    session.history.append(history_entry)
    session.questions_answered += 1
    
    # Check completion
    test_completed = session.questions_answered >= TEST_LENGTH
    if test_completed:
        session.completed = True
        logger.info(f"Session {session_id} completed test.")
        
    update_session(session)
    
    result = {
        "correct": is_correct,
        "ability": session.ability_score
    }
    
    if test_completed:
        result["test_completed"] = True
    else:
        asked_ids = [h.question_id for h in session.history]
        next_question = select_next_question(session.ability_score, asked_ids)
        result["next_question"] = {
            "question_id": next_question.id,
            "question": next_question.question,
            "options": next_question.options,
            "difficulty": next_question.difficulty
        }
        logger.info(f"Question served to {session_id} - Difficulty: {next_question.difficulty}")
        
    return result
