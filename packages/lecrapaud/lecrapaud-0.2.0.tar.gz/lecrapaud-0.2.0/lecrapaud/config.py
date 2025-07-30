import os
from dotenv import load_dotenv

load_dotenv(override=False)

PYTHON_ENV = os.getenv("PYTHON_ENV")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
EMAIL = os.getenv("EMAIL")
DATASET_ID = os.getenv("DATASET_ID")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
USERNAME = os.getenv("USERNAME")
FRAISE = os.getenv("FRAISE")
FA2 = os.getenv("2FA")
INT = os.getenv("INT")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
ALPHA_VENTAGE_API_KEY = os.getenv("ALPHA_VENTAGE_API_KEY")

DB_USER = os.getenv("TEST_DB_USER") if PYTHON_ENV == "Test" else os.getenv("DB_USER")
DB_PASSWORD = (
    os.getenv("TEST_DB_PASSWORD") if PYTHON_ENV == "Test" else os.getenv("DB_PASSWORD")
)
DB_HOST = os.getenv("TEST_DB_HOST") if PYTHON_ENV == "Test" else os.getenv("DB_HOST")
DB_PORT = os.getenv("TEST_DB_PORT") if PYTHON_ENV == "Test" else os.getenv("DB_PORT")
DB_NAME = os.getenv("TEST_DB_NAME") if PYTHON_ENV == "Test" else os.getenv("DB_NAME")
DB_URI = os.getenv("DB_URI", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
