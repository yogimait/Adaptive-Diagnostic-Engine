import logging
from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from app.config import MONGO_URI, DATABASE_NAME

logger = logging.getLogger(__name__)

# Initialize MongoClient
client = MongoClient(MONGO_URI)
db: Database = client[DATABASE_NAME]

def get_questions_collection() -> Collection:
    return db["questions"]

def get_sessions_collection() -> Collection:
    return db["sessions"]

def init_db():
    logger.info("Initializing database and creating indexes...")
    questions_col = get_questions_collection()
    
    # Create indexes for optimized querying
    # 1. Index on difficulty
    questions_col.create_index([("difficulty", ASCENDING)])
    # 2. Index on topic
    questions_col.create_index([("topic", ASCENDING)])
    
    logger.info("Database indexes successfully configured.")
