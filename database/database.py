import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

# Ensure the parent directory for the SQLite database exists
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

# Create engine. Connect_args is only needed for SQLite.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite://") else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Declarative Base model
Base = declarative_base()

def init_db() -> None:
    """
    Import models and create all database tables.
    """
    import database.models  # noqa: F401
    Base.metadata.create_all(bind=engine)

# Track if the database has been initialized
_db_initialized = False

def get_db():
    """
    Dependency helper to retrieve a database session.
    Automatically initializes the database tables on the first connection.
    """
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
