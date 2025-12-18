"""Database configuration and session management for FastAPI"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create base class for models
Base = declarative_base()

# Database engine and session maker - initialized on first use
_engine = None
_SessionLocal = None

def get_engine():
    """Get or create database engine"""
    global _engine
    if _engine is None:
        from config import get_config
        settings = get_config()
        _engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.SQLALCHEMY_ECHO,
            pool_pre_ping=True,
        )
    return _engine

def get_session_local():
    """Get or create session maker"""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal

def get_db():
    """Dependency to get database session"""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

