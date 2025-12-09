import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

try:
    # Load environment variables from a .env file when present.
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass


def _build_engine() -> Engine:
    db_url = os.getenv("DB_URL")
    if not db_url:
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD")
        database = os.getenv("POSTGRES_DB") or os.getenv("POSTGRES_DATABASE")

        if not database:
            raise RuntimeError("DB_URL or POSTGRES_DB is required to create the database engine")

        auth = user
        if password:
            auth = f"{auth}:{password}"
        db_url = f"postgresql+psycopg2://{auth}@{host}:{port}/{database}"

    if not db_url:
        raise RuntimeError("DB_URL is required to create the database engine")

    schema = os.getenv("POSTGRES_SCHEMA")
    connect_args = {"options": f"-csearch_path={schema}"} if schema else {}

    return create_engine(
        db_url,
        pool_size=5,
        max_overflow=5,
        pool_pre_ping=True,
        connect_args=connect_args,
        future=True,
    )


_engine = _build_engine()
_SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False)


def create_db() -> Generator[Session, None, None]:
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
