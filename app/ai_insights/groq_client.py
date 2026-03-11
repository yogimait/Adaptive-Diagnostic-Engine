import logging
from groq import Groq
from app.config import GROQ_API_KEY

logger = logging.getLogger(__name__)

def generate_study_plan_from_groq(prompt: str) -> str:
    if not GROQ_API_KEY:
        logger.warning("Groq API key is missing.")
        return "Groq API key missing."

    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an educational diagnostic assistant.

Your task is to produce a short 3-step study plan.


Rules:
- Output exactly 3 numbered steps.
- Each step must be one concise sentence.
- Focus only on the student's weak topics.
- Do not reason or explain.
- Do not include analysis.

Output format (STRICT):

1. Step one
2. Step two
3. Step three


Only return the three numbered steps.
"""
},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=300
        )

        text = response.choices[0].message.content.strip()

        # fallback if model produced empty output
        if not text:
            return (
                "1. Review foundational concepts in the weak topics.\n"
                "2. Practice targeted problems focusing on those areas.\n"
                "3. Take short quizzes regularly to reinforce understanding."
            )

        text = text.replace("\n\n", "\n")
        text = text.replace("\u2011", "-")
        return text

    except Exception as e:
        logger.error(f"Groq API error: {str(e)}")
        return f"Groq API error: {str(e)}"