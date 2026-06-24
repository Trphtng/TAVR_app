from typing import List, Optional
from sqlalchemy.orm import Session
from database.models import Vocabulary

def create_vocabulary(db: Session, data: dict) -> Vocabulary:
    """
    Creates a new vocabulary record in the database.
    """
    db_vocab = Vocabulary(**data)
    db.add(db_vocab)
    db.commit()
    db.refresh(db_vocab)
    return db_vocab

def get_vocabulary_by_id(db: Session, id: int) -> Optional[Vocabulary]:
    """
    Retrieves a vocabulary record by its unique ID.
    """
    return db.query(Vocabulary).filter(Vocabulary.id == id).first()

def search_vocabulary(db: Session, keyword: str) -> List[Vocabulary]:
    """
    Searches vocabulary records matching the keyword in word, topic, or context.
    """
    search_pattern = f"%{keyword}%"
    return db.query(Vocabulary).filter(
        Vocabulary.word.ilike(search_pattern) |
        Vocabulary.topic.ilike(search_pattern) |
        Vocabulary.context.ilike(search_pattern)
    ).all()

def get_all_vocabulary(db: Session) -> List[Vocabulary]:
    """
    Retrieves all vocabulary records from the database.
    """
    return db.query(Vocabulary).all()
