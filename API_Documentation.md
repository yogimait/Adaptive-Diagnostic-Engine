# API Documentation

This service strictly utilizes JSON-encoded configurations. Ensure `Content-Type: application/json` headers are properly provided where applicable. 

**Base URL**: `http://localhost:8000`

## System Workflow

1. A user starts a session via `/start-session`.
2. The system initializes the ability score at 0.5.
3. A question close to the current ability is served.
4. The user submits an answer via `/submit-answer`.
5. The ability score updates depending on correctness.
6. The next question difficulty adjusts accordingly.
7. After 10 questions, the session completes.
8. Weak topics are identified and an AI study plan is generated.
---

## `GET /health`
Returns the status of the generic backend process to ensure the service is responsive. 

**Response**
```json
{
  "status": "ok"
}
```

---

## `POST /start-session`
Initializes a new tracking session instance and returns the foundational question baseline (0.5 difficulty).

**Response**
```json
{
  "session_id": "ab12-cd34-...",
  "question_id": "ef56-gh78-...",
  "question": "What is x if 2x = 10?",
  "options": ["4", "5", "6", "10"],
  "difficulty": 0.5
}
```

---

## `POST /submit-answer`
Commits a multiple-choice string answer, inherently recalculating and progressing the internal adaptive difficulty states.

**Request Body**
```json
{
  "session_id": "ab12-cd34-...",
  "question_id": "ef56-gh78-...",
  "answer": "5"
}
```

**Response (In-Progress)**
```json
{
  "correct": true,
  "ability": 0.6,
  "next_question": {
     "question_id": "ij90-kl12-...",
     "question": "What is x if x^2 - 4x + 4 = 0?",
     "options": ["-2", "2", "4", "0"],
     "difficulty": 0.6
  }
}
```

**Response (Upon Completion)**
```json
{
  "correct": true,
  "ability": 0.75,
  "test_completed": true
}
```

---

## `GET /result/{session_id}`
Compiles and streams the finalized analytics of a finished sequential test array via the Session ID. 
*(Note: Attempting to call this endpoint prior to the session finishing execution naturally will throw a 400 Bad Request HTTP exception).*

**Response**
```json
{
  "ability_score": 0.75,
  "questions_answered": 10,
  "accuracy": 80.0,
  "weak_topics": ["Geometry"],
  "study_plan": "1. Review fundamental geometric formulas...\n2. Practice right triangle identification..."
}
```

---

## Internal Usage Endpoints
### `GET /questions/count`
Diagnostic utility for verifying seed operation integrity by counting loaded database configurations.
```json
{
  "total_questions": 20
}
```
