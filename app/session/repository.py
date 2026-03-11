from typing import Optional
from app.database import get_sessions_collection
from app.session.model import Session

def create_session(session: Session):
    col = get_sessions_collection()
    data = session.model_dump(by_alias=True)
    col.insert_one(data)

def get_session(session_id: str) -> Optional[Session]:
    col = get_sessions_collection()
    data = col.find_one({"_id": session_id})
    if data:
        return Session(**data)
    return None

def update_session(session: Session):
    col = get_sessions_collection()
    col.update_one(
        {"_id": session.session_id},
        {"$set": session.model_dump(by_alias=True)}
    )
