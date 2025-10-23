import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def _build_engine():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return create_engine(database_url, pool_pre_ping=True)

    db_dir = os.getenv("DB_DIR", "/opt/data")
    os.makedirs(db_dir, exist_ok=True)
    sqlite_url = f"sqlite:///{db_dir}/carts.db"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})


engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
