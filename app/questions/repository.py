import random
from typing import List, Optional
from app.database import get_questions_collection
from app.questions.model import QuestionDB

def get_question_by_id(question_id: str) -> Optional[QuestionDB]:
    col = get_questions_collection()
    data = col.find_one({"_id": question_id})
    if data:
        return QuestionDB(**data)
    return None

def count_questions() -> int:
    return get_questions_collection().count_documents({})

def get_random_question_near_difficulty(ability: float, exclude_ids: List[str]) -> Optional[QuestionDB]:
    col = get_questions_collection()
    
    # Progressively widen the search range
    ranges = [0.05, 0.1, 0.2, 0.3, 1.0] # 1.0 added as absolute fallback to ensure a question is always found if possible
    
    for r in ranges:
        min_diff = max(0.1, ability - r)
        max_diff = min(1.0, ability + r)
        
        query = {
            "difficulty": {"$gte": min_diff, "$lte": max_diff},
            "_id": {"$nin": exclude_ids}
        }
        
        matching_questions = list(col.find(query))
        
        if matching_questions:
            selected = random.choice(matching_questions)
            return QuestionDB(**selected)
            
    return None
