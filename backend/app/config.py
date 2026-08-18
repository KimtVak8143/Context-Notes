import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI") or os.getenv("DATABASE_URL") or "mongodb://localhost:27017/context"
MONGODB_DB = os.getenv("MONGODB_DB") or "context"
USE_IN_MEMORY_DB = os.getenv("USE_IN_MEMORY_DB", "0").lower() in {"1", "true", "yes", "on"}
