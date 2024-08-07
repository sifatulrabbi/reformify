import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", "localhost")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "localhost")
DB_PASS = os.getenv("DB_PASS", "localhost")
DB_USER = os.getenv("DB_USER", "localhost")
DB_DRIVER = os.getenv("DB_DRIVER", "localhost")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)


if not JWT_SECRET_KEY:
    raise Exception("JWT_SECRET_KEY env is required")
