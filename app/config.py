from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "adaptive_testing")
TEST_LENGTH = int(os.getenv("TEST_LENGTH", 10))
ABILITY_START = float(os.getenv("ABILITY_START", 0.5))
ABILITY_STEP = float(os.getenv("ABILITY_STEP", 0.1))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Ensure API Key is populated if needed, though we will handle missing gracefully or assert later
