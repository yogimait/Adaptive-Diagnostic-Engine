from app.questions.repository import get_questions_near_difficulty


def select_next_question(ability: float, asked_ids: list):
    """
    Select a question near the user's ability
    while avoiding previously asked questions.
    """

    search_ranges = [0.05, 0.1, 0.2, 0.3]

    for r in search_ranges:
        questions = get_questions_near_difficulty(ability, r, asked_ids)

        if questions:
            return questions[0]

    return None