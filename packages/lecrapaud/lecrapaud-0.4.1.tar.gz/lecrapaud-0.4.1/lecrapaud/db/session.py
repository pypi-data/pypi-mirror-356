"""Database session management and initialization module."""

from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from alembic.config import Config
from alembic import command
import os

from lecrapaud.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_URI

_engine = None
_SessionLocal = None
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" or DB_URI
)


def init_db(uri: str = None):
    global _engine, _SessionLocal

    uri = uri if uri else DATABASE_URL
    # Extract DB name from URI to connect without it
    parsed = urlparse(uri)
    db_name = parsed.path.lstrip("/")  # remove leading slash

    # Build root engine (no database in URI)
    root_uri = uri.replace(f"/{db_name}", "/")

    # Step 1: Connect to MySQL without a database
    root_engine = create_engine(root_uri)

    # Step 2: Create database if it doesn't exist
    with root_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()

    # Step 3: Connect to the newly created database
    _engine = create_engine(uri, echo=False)

    # Step 4: Create session factory
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    # Step 5: Apply Alembic migrations programmatically
    project_root = os.path.abspath(os.path.dirname(__file__))
    alembic_cfg_path = os.path.join(project_root, "alembic.ini")

    alembic_cfg = Config(alembic_cfg_path)
    alembic_cfg.set_main_option("sqlalchemy.url", uri or os.getenv("DATABASE_URL"))
    command.upgrade(alembic_cfg, "head")


# Dependency to get a session instance
@contextmanager
def get_db():
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call `init_db()` first.")
    db = _SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise Exception(e) from e
    finally:
        db.close()
