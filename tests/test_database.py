import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base
from database.models import Vocabulary
from services.vocabulary_service import (
    create_vocabulary,
    get_vocabulary_by_id,
    search_vocabulary,
    get_all_vocabulary
)

# Use in-memory SQLite database for test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="db_session")
def fixture_db_session():
    # Setup test database engine and session
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables defined on Base
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_database_and_services(db_session):
    # 1. Create/insert vocabulary record
    vocab_data = {
        "word": "decorator",
        "context": "Python decorators are a clean way to wrap functions.",
        "source": "Python documentation",
        "translation_vi": "bộ trang trí / hàm bao",
        "translation_en": "wrapper function modifying another function",
        "technical_vi": "hàm trang trí",
        "technical_en": "a design pattern that allows user to add new functionality to an existing object without modifying its structure",
        "simple_en": "a wrapper to change function behavior",
        "simple_vi": "một bộ bao để thay đổi hành vi hàm",
        "example_en": "@my_decorator def my_func(): pass",
        "example_vi": "@my_decorator định nghĩa hàm của tôi",
        "topic": "Python"
    }
    
    created = create_vocabulary(db_session, vocab_data)
    
    # Assertions for Insertion
    assert created.id is not None
    assert created.word == "decorator"
    assert created.created_at is not None

    # 2. Query record
    retrieved = get_vocabulary_by_id(db_session, created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.word == "decorator"
    assert retrieved.topic == "Python"

    # 3. Search record
    # Search by word segment
    search_results = search_vocabulary(db_session, "decor")
    assert len(search_results) == 1
    assert search_results[0].id == created.id

    # Search by topic segment
    search_results_topic = search_vocabulary(db_session, "python")
    assert len(search_results_topic) == 1

    # Search by non-existent word
    search_results_empty = search_vocabulary(db_session, "nonexistent")
    assert len(search_results_empty) == 0

    # 4. Get all records
    all_vocab = get_all_vocabulary(db_session)
    assert len(all_vocab) == 1
    assert all_vocab[0].word == "decorator"
