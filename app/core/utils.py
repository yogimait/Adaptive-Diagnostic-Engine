import uuid
from datetime import datetime, timezone

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamps a value between a minimum and maximum bound."""
    return max(min_val, min(value, max_val))

def generate_session_id() -> str:
    """Generates a unique identifier for a user session."""
    return str(uuid.uuid4())

def current_timestamp() -> str:
    """Returns the current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()
