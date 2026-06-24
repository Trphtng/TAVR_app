from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.models import Vocabulary

def get_now() -> datetime:
    """
    Returns the current time in UTC as a timezone-naive object
    to ensure database column compatibility.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)

def generate_next_review_date(review_count: int, rating: str) -> datetime:
    """
    Generates the next review date based on spaced repetition rules.
    - 'easy' expands the spacing interval exponentially.
    - 'hard' schedules the word for review in 1 hour.
    """
    now = get_now()
    if rating == "easy":
        if review_count == 0:
            return now + timedelta(days=1)
        elif review_count == 1:
            return now + timedelta(days=4)
        else:
            days = 4 * (2 ** (review_count - 1))
            return now + timedelta(days=min(days, 365))  # Cap at 1 year
    else:  # hard
        # Review again in 1 hour
        return now + timedelta(hours=1)

def get_review_words(db: Session) -> list:
    """
    Retrieves all vocabulary words that are due for review.
    A word is due if its next_review date is in the past (<= now) or is None (new word).
    """
    now = get_now()
    return db.query(Vocabulary).filter(
        or_(
            Vocabulary.next_review.is_(None),
            Vocabulary.next_review <= now
        )
    ).all()

def mark_easy(db: Session, vocab: Vocabulary) -> None:
    """
    Marks a vocabulary word as 'easy' and schedules its next review.
    """
    now = get_now()
    vocab.next_review = generate_next_review_date(vocab.review_count, "easy")
    vocab.last_review = now
    vocab.review_count += 1
    vocab.difficulty = max(0, (vocab.difficulty or 0) - 1)
    vocab.status = "learned" if vocab.review_count > 2 else "learning"
    db.commit()

def mark_hard(db: Session, vocab: Vocabulary) -> None:
    """
    Marks a vocabulary word as 'hard' and reschedules its next review soon.
    """
    now = get_now()
    vocab.next_review = generate_next_review_date(vocab.review_count, "hard")
    vocab.last_review = now
    vocab.review_count = 0  # Reset interval progression
    vocab.difficulty = min(5, (vocab.difficulty or 0) + 1)
    vocab.status = "learning"
    db.commit()
