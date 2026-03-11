import os
import sys
import logging
from pymongo import MongoClient
import uuid

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import MONGO_URI, DATABASE_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_seed_data():
    questions = [
        # Algebra - Easy (0.2)
        {"question": "What is x if 2x = 10?", "options": ["4", "5", "6", "10"], "correct_answer": "5", "difficulty": 0.2, "topic": "Algebra", "tags": ["linear equations"]},
        {"question": "Solve for y: y + 3 = 10", "options": ["5", "6", "7", "8"], "correct_answer": "7", "difficulty": 0.2, "topic": "Algebra", "tags": ["linear equations"]},
        
        # Algebra - Medium (0.5)
        {"question": "What is x if 3x - 5 = 10?", "options": ["3", "4", "5", "6"], "correct_answer": "5", "difficulty": 0.5, "topic": "Algebra", "tags": ["linear equations"]},
        {"question": "Solve: 2(x + 3) = 14", "options": ["4", "5", "6", "7"], "correct_answer": "4", "difficulty": 0.5, "topic": "Algebra", "tags": ["linear equations"]},
        
        # Algebra - Hard (0.8)
        {"question": "What is x if x^2 - 4x + 4 = 0?", "options": ["-2", "2", "4", "0"], "correct_answer": "2", "difficulty": 0.8, "topic": "Algebra", "tags": ["quadratic equations"]},
        
        # Geometry - Easy (0.2)
        {"question": "How many sides does a triangle have?", "options": ["2", "3", "4", "5"], "correct_answer": "3", "difficulty": 0.2, "topic": "Geometry", "tags": ["shapes"]},
        {"question": "What is the sum of angles in a triangle?", "options": ["90", "180", "270", "360"], "correct_answer": "180", "difficulty": 0.2, "topic": "Geometry", "tags": ["angles"]},
        
        # Geometry - Medium (0.5)
        {"question": "What is the area of a square with side 4?", "options": ["8", "12", "16", "20"], "correct_answer": "16", "difficulty": 0.5, "topic": "Geometry", "tags": ["area"]},
        {"question": "What is the perimeter of a rectangle with sides 3 and 4?", "options": ["7", "12", "14", "16"], "correct_answer": "14", "difficulty": 0.5, "topic": "Geometry", "tags": ["perimeter"]},
        
        # Geometry - Hard (0.8)
        {"question": "What is the hypotenuse of a right triangle with legs 3 and 4?", "options": ["5", "6", "7", "12"], "correct_answer": "5", "difficulty": 0.8, "topic": "Geometry", "tags": ["pythagorean theorem"]},
        
        # Arithmetic - Easy (0.2)
        {"question": "What is 7 + 8?", "options": ["13", "14", "15", "16"], "correct_answer": "15", "difficulty": 0.2, "topic": "Arithmetic", "tags": ["addition"]},
        {"question": "What is 20 - 9?", "options": ["9", "10", "11", "12"], "correct_answer": "11", "difficulty": 0.2, "topic": "Arithmetic", "tags": ["subtraction"]},
        
        # Arithmetic - Medium (0.5)
        {"question": "What is 12 * 12?", "options": ["124", "134", "144", "154"], "correct_answer": "144", "difficulty": 0.5, "topic": "Arithmetic", "tags": ["multiplication"]},
        {"question": "What is 144 / 12?", "options": ["10", "11", "12", "14"], "correct_answer": "12", "difficulty": 0.5, "topic": "Arithmetic", "tags": ["division"]},
        {"question": "What is 15% of 200?", "options": ["15", "20", "30", "45"], "correct_answer": "30", "difficulty": 0.5, "topic": "Arithmetic", "tags": ["percentages"]},
        
        # Arithmetic - Hard (0.8)
        {"question": "Calculate: (1/3) + (1/6)", "options": ["1/9", "2/9", "3/6", "1/2"], "correct_answer": "1/2", "difficulty": 0.8, "topic": "Arithmetic", "tags": ["fractions"]},
        {"question": "What is the cube root of 343?", "options": ["6", "7", "8", "9"], "correct_answer": "7", "difficulty": 0.8, "topic": "Arithmetic", "tags": ["roots"]},
        
        # Vocabulary - Medium (0.5)
        {"question": "What is a synonym for 'Abundant'?", "options": ["Scarce", "Plentiful", "Rare", "Thin"], "correct_answer": "Plentiful", "difficulty": 0.5, "topic": "Vocabulary", "tags": ["synonyms"]},
        {"question": "What is an antonym for 'Expand'?", "options": ["Grow", "Stretch", "Contract", "Inflate"], "correct_answer": "Contract", "difficulty": 0.5, "topic": "Vocabulary", "tags": ["antonyms"]},
        
        # Vocabulary - Hard (0.8)
        {"question": "What does the word 'Ephemeral' mean?", "options": ["Long-lasting", "Short-lived", "Luminous", "Heavy"], "correct_answer": "Short-lived", "difficulty": 0.8, "topic": "Vocabulary", "tags": ["definitions"]}
    ]
    
    # ensure each has a unique string _id
    for q in questions:
        q["_id"] = str(uuid.uuid4())
        
    return questions

def seed():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    col = db["questions"]
    
    logger.info("Dropping existing questions...")
    col.drop()
    
    questions = generate_seed_data()
    logger.info(f"Inserting {len(questions)} seed questions...")
    col.insert_many(questions)
    
    # Print out distribution
    from collections import Counter
    diff_counts = dict(Counter(q["difficulty"] for q in questions))
    topic_counts = dict(Counter(q["topic"] for q in questions))
    logger.info(f"Difficulty distribution: {diff_counts}")
    logger.info(f"Topic distribution: {topic_counts}")
    
    logger.info("Seed complete.")

if __name__ == "__main__":
    seed()
