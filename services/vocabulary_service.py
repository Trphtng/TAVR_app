from typing import List, Optional
from sqlalchemy.orm import Session
from database.models import Vocabulary

def map_ai_to_db_format(data: dict) -> dict:
    """
    Maps AI service returned keys to database model field names.
    """
    return {
        "word": data.get("word", ""),
        "context": data.get("context", ""),
        "source": data.get("source", ""),
        "translation_vi": data.get("translation_vi", ""),
        "translation_en": data.get("translation_en", ""),
        "technical_vi": data.get("technical_explanation_vi") or data.get("technical_vi", ""),
        "technical_en": data.get("technical_explanation_en") or data.get("technical_en", ""),
        "simple_vi": data.get("simple_explanation_vi") or data.get("simple_vi", ""),
        "simple_en": data.get("simple_explanation_en") or data.get("simple_en", ""),
        "example_en": data.get("example_en", ""),
        "example_vi": data.get("example_vi", ""),
        "topic": data.get("topic", "")
    }

def create_vocabulary(db: Session, data: dict) -> Vocabulary:
    """
    Creates a new vocabulary record in the database.
    Automatically maps AI-structured fields to database schema fields.
    """
    mapped_data = map_ai_to_db_format(data)
    db_vocab = Vocabulary(**mapped_data)
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
