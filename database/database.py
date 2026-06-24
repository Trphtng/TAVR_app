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
    Import models, create all database tables, and run schema migration inspections.
    """
    import database.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    
    # Simple migration: dynamically add columns to existing table if they don't exist
    from sqlalchemy import inspect, text
    inspector = inspect(engine)
    if "vocabulary" in inspector.get_table_names():
        existing_columns = [col["name"] for col in inspector.get_columns("vocabulary")]
        
        new_columns = {
            "difficulty": "INTEGER DEFAULT 0",
            "status": "VARCHAR DEFAULT 'new'",
            "review_count": "INTEGER DEFAULT 0",
            "next_review": "DATETIME",
            "last_review": "DATETIME"
        }
        
        with engine.begin() as conn:
            for col_name, col_type in new_columns.items():
                if col_name not in existing_columns:
                    conn.execute(text(f"ALTER TABLE vocabulary ADD COLUMN {col_name} {col_type}"))


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
