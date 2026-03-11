from app.config import ABILITY_STEP
from app.core.utils import clamp

def calculate_new_ability(current_ability: float, is_correct: bool) -> float:
    """
    Updates the ability score based on correctness.
    Includes optional enhancement: smaller step changes near edges.
    """
    step = ABILITY_STEP
    
    # Smaller steps near edges to conservatively move difficulty
    if current_ability > 0.9 and is_correct:
        step = ABILITY_STEP / 2
    elif current_ability < 0.2 and not is_correct:
        step = ABILITY_STEP / 2
        
    if is_correct:
        new_ability = current_ability + step
    else:
        new_ability = current_ability - step
        
    return round(clamp(new_ability, 0.1, 1.0), 2)
