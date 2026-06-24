from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from database.database import Base

class Vocabulary(Base):
    """
    SQLAlchemy ORM model representing the 'vocabulary' table.
    Stores user-selected technical words along with their context, translations,
    and explanations.
    """
    __tablename__ = "vocabulary"

    id: int = Column(Integer, primary_key=True, index=True)
    word: str = Column(String, nullable=False, index=True)
    context: Optional[str] = Column(String, nullable=True)
    source: Optional[str] = Column(String, nullable=True)

    translation_vi: Optional[str] = Column(String, nullable=True)
    translation_en: Optional[str] = Column(String, nullable=True)

    technical_vi: Optional[str] = Column(String, nullable=True)
    technical_en: Optional[str] = Column(String, nullable=True)

    simple_en: Optional[str] = Column(String, nullable=True)
    simple_vi: Optional[str] = Column(String, nullable=True)

    example_en: Optional[str] = Column(String, nullable=True)
    example_vi: Optional[str] = Column(String, nullable=True)

    topic: Optional[str] = Column(String, nullable=True, index=True)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

