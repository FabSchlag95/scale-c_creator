import os
from typing import Optional

from sqlalchemy import text
from sqlalchemy.engine import Engine

from db import tables
from db.create_engine import _build_engine


def _get_metadata():
    """Return SQLAlchemy metadata from the tables module."""
    metadata = getattr(tables, "metadata", None)
    if metadata is not None and hasattr(metadata, "create_all"):
        return metadata

    base = getattr(tables, "Base", None)
    if base is not None and hasattr(base, "metadata"):
        return base.metadata

    raise RuntimeError("No SQLAlchemy metadata found in db.tables")


def _ensure_schema(engine: Engine, schema: Optional[str]) -> None:
    if not schema:
        return

    safe_schema = schema.replace('"', '""')
    with engine.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{safe_schema}"'))
        conn.commit()


def init_db() -> None:
    engine = _build_engine()
    schema = os.getenv("DB_SCHEMA") or os.getenv("POSTGRES_SCHEMA")

    _ensure_schema(engine, schema)
    metadata = _get_metadata()
    metadata.create_all(bind=engine, checkfirst=True)


if __name__ == "__main__":
    init_db()
