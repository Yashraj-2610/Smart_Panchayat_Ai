from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Fix postgres:// URL scheme for SQLAlchemy (Render provides postgres://)
database_url = settings.DATABASE_URL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Connection pooling configuration for better performance
engine_config = {
    "pool_pre_ping": True,  # Verify connections before using
    "pool_recycle": 3600,   # Recycle connections after 1 hour
    "pool_size": 10,        # Connection pool size
    "max_overflow": 20,     # Max connections beyond pool_size
    "echo": False,          # Set to True for SQL query logging
}

# SQLite needs check_same_thread, PostgreSQL doesn't
if "sqlite" in database_url:
    engine_config["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_config)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
