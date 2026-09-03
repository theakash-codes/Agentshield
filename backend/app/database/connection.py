import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Load .env from the project root
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False
)


# Create database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)