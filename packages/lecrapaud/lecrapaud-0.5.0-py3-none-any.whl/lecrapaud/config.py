import os
from dotenv import load_dotenv

load_dotenv(override=False)

PYTHON_ENV = os.getenv("PYTHON_ENV")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DATASET_ID = os.getenv("DATASET_ID")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

DB_USER = (
    os.getenv("TEST_DB_USER") if PYTHON_ENV == "Test" else os.getenv("DB_USER", None)
)
DB_PASSWORD = (
    os.getenv("TEST_DB_PASSWORD")
    if PYTHON_ENV == "Test"
    else os.getenv("DB_PASSWORD", None)
)
DB_HOST = (
    os.getenv("TEST_DB_HOST") if PYTHON_ENV == "Test" else os.getenv("DB_HOST", None)
)
DB_PORT = (
    os.getenv("TEST_DB_PORT") if PYTHON_ENV == "Test" else os.getenv("DB_PORT", None)
)
DB_NAME = (
    os.getenv("TEST_DB_NAME") if PYTHON_ENV == "Test" else os.getenv("DB_NAME", None)
)
DB_URI = os.getenv("DB_URI", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
