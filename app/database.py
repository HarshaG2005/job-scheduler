import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# Fly.io Postgres URLs (postgres:// -> postgresql+psycopg://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

# Lazy loading pattern
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL, 
            pool_pre_ping=True, 
            pool_recycle=3600
        )
    return _engine

SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=get_engine()
    )
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
