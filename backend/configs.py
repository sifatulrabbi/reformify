import os
from dotenv import load_dotenv

load_dotenv()


PORT = os.getenv("PORT", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_NAME = os.getenv("DB_NAME", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_USER = os.getenv("DB_USER", None)
DB_DRIVER = os.getenv("DB_DRIVER", None)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", None)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"


if not JWT_SECRET_KEY:
    raise Exception("JWT_SECRET_KEY env is required")
if not DB_HOST:
    raise Exception("DB_HOST env is required")
if not DB_NAME:
    raise Exception("DB_NAME env is required")
if not DB_PASS:
    raise Exception("DB_PASS env is required")
if not DB_USER:
    raise Exception("DB_USER env is required")
if not DB_DRIVER:
    raise Exception("DB_DRIVER env is required")
if not INTERNAL_API_KEY:
    raise Exception("INTERNAL_API_KEY env is required")
