import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base
from database.models import Vocabulary
from services.learning_service import (
    generate_next_review_date,
    get_review_words,
    mark_easy,
    mark_hard,
    get_now
)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="db_session")
def fixture_db_session():
    # Setup test database engine and session
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_generate_next_review_date():
    """
    Verify interval calculations for Easy and Hard ratings.
    """
    now = get_now()
    
    # Easy cases
    date_easy_0 = generate_next_review_date(0, "easy")
    assert (date_easy_0 - now).days == 1
    
    date_easy_1 = generate_next_review_date(1, "easy")
    assert (date_easy_1 - now).days == 4
    
    date_easy_2 = generate_next_review_date(2, "easy")
    assert (date_easy_2 - now).days == 8

    # Hard case (schedules in 1 hour)
    date_hard = generate_next_review_date(0, "hard")
    assert abs((date_hard - now).total_seconds() - 3600) < 5

def test_learning_flow(db_session):
    """
    Verify full workflow of spaced repetition due queries and metadata updates.
    """
    # 1. Create a new vocabulary word (next_review starts as None)
    vocab = Vocabulary(
        word="testing",
        translation_vi="kiểm thử",
        translation_en="testing",
        review_count=0,
        next_review=None
    )
    db_session.add(vocab)
    db_session.commit()
    db_session.refresh(vocab)
    
    # New word must be returned as due
    due_words = get_review_words(db_session)
    assert len(due_words) == 1
    assert due_words[0].word == "testing"
    
    # 2. Mark easy (schedules next review in 1 day)
    mark_easy(db_session, vocab)
    assert vocab.review_count == 1
    assert vocab.difficulty == 0
    assert vocab.status == "learning"
    assert vocab.next_review is not None
    assert vocab.last_review is not None
    
    # The word is scheduled for tomorrow, so it should not be due now
    due_words_after_easy = get_review_words(db_session)
    assert len(due_words_after_easy) == 0
    
    # 3. Mark hard (resets count to 0 and increases difficulty)
    mark_hard(db_session, vocab)
    assert vocab.review_count == 0
    assert vocab.difficulty == 1
    assert vocab.status == "learning"
