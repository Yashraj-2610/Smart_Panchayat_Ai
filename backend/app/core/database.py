"""
Database configuration with enhanced connection pooling
Supports SQLite (development) and PostgreSQL (production)
"""
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from typing import Optional
import logging

from .config import settings

logger = logging.getLogger(__name__)


def _normalize_database_url(url: str) -> str:
    """Normalize database URL (Render provides postgres:// instead of postgresql://)"""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def _build_engine(database_url: str):
    """Build SQLAlchemy engine with appropriate configuration"""
    database_url = _normalize_database_url(database_url)
    is_sqlite = "sqlite" in database_url

    engine_config = {
        "echo": False,  # Set to True for SQL query logging
    }

    if is_sqlite:
        # SQLite: single connection, check_same_thread=False for Streamlit
        engine_config["connect_args"] = {"check_same_thread": False}
        engine_config["poolclass"] = NullPool
    else:
        # PostgreSQL/MySQL: connection pooling
        engine_config.update({
            "pool_pre_ping": True,  # Verify connections before using
            "pool_recycle": 3600,   # Recycle connections after 1 hour
            "pool_size": 10,        # Connection pool size
            "max_overflow": 20,     # Max connections beyond pool_size
            "pool_timeout": 30,     # Timeout for getting connection
            "poolclass": QueuePool,
        })

    engine = create_engine(database_url, **engine_config)
    return engine


# Create engine with settings
DATABASE_URL = _normalize_database_url(settings.DATABASE_URL)
engine = _build_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Database session dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_health() -> dict:
    """
    Check database connectivity and basic health status
    Returns dict with health information
    """
    health_info = {
        "database_type": "sqlite" if "sqlite" in DATABASE_URL else "postgresql",
        "database_url_set": bool(DATABASE_URL),
        "connected": False,
        "error": None,
    }

    try:
        with engine.connect() as conn:
            # Simple connectivity check
            if "sqlite" in DATABASE_URL:
                conn.execute(text("SELECT 1"))
            else:
                conn.execute(text("SELECT 1"))

            # Get table count
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            health_info["tables_count"] = len(tables)
            health_info["tables"] = tables[:10]  # Limit for response size
            health_info["connected"] = True
    except Exception as e:
        health_info["error"] = str(e)
        logger.error(f"Database health check failed: {e}")

    return health_info


def get_database_stats() -> dict:
    """Get database statistics for monitoring"""
    stats = {
        "database_type": "sqlite" if "sqlite" in DATABASE_URL else "postgresql",
        "pool_size": getattr(engine.pool, "size", lambda: 0)() if hasattr(engine.pool, "size") else 0,
    }

    try:
        with engine.connect() as conn:
            if "sqlite" in DATABASE_URL:
                result = conn.execute(text("SELECT COUNT(*) FROM sqlite_master WHERE type='table'"))
                stats["table_count"] = result.scalar()
            else:
                result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables"))
                stats["table_count"] = result.scalar()
    except Exception as e:
        stats["error"] = str(e)

    return stats