from app.session.repository import get_session
from app.core.errors import SessionNotFound, ResultNotReadyError
from app.ai_insights.groq_client import generate_study_plan_from_groq

def get_session_result_and_plan(session_id: str) -> dict:
    session = get_session(session_id)
    if not session:
        raise SessionNotFound()
        
    if not session.completed:
        raise ResultNotReadyError()
        
    total_questions = session.questions_answered
    correct_count = sum(1 for h in session.history if h.correct)
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0.0
    
    # Calculate weak topics
    topic_performance = {}
    for h in session.history:
        if h.topic not in topic_performance:
            topic_performance[h.topic] = {"total": 0, "correct": 0}
        topic_performance[h.topic]["total"] += 1
        if h.correct:
            topic_performance[h.topic]["correct"] += 1
            
    weak_topics = []
    for topic, stats in topic_performance.items():
        # Consider a topic weak if accuracy in that topic is less than 60%
        topic_accuracy = stats["correct"] / stats["total"]
        if topic_accuracy < 0.6:
            weak_topics.append(topic)
            
    # If no explicitly weak topics, find the one with the lowest accuracy
    if not weak_topics and topic_performance:
        weakest = min(topic_performance.keys(), key=lambda t: topic_performance[t]["correct"]/topic_performance[t]["total"])
        weak_topics.append(weakest)
        
    prompt = f"""
Student ability score: {session.ability_score:.2f}
Weak topics: {', '.join(weak_topics) if weak_topics else 'None'}
Correct answers: {correct_count}/{total_questions}

Generate a concise 3-step study plan for this student.

Return exactly:

1. Step
2. Step
3. Step

No markdown.
No titles.
No bullet symbols.
    """
    
    study_plan = generate_study_plan_from_groq(prompt)
    
    return {
        "ability_score": session.ability_score,
        "questions_answered": total_questions,
        "accuracy": accuracy,
        "weak_topics": weak_topics,
        "study_plan": study_plan
    }
