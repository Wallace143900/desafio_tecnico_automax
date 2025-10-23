import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_DIR = os.getenv("DB_DIR", "/opt/data")
os.makedirs(DB_DIR, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_DIR}/carts.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
