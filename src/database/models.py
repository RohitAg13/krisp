from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime


class Summary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    summary_type: str  # extractive or abstractive
    summary: Optional[str] = None
    highlights: Optional[List["Highlight"]] = Relationship(
        back_populates="summary",
    )
    word_count: Optional[int]
    summary_word_count: Optional[int]
    response_time: Optional[float]
    created_at: datetime = datetime.utcnow()


class Highlight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    highlight: str

    summary_id: Optional[int] = Field(default=None, foreign_key="summary.id")
    summary: Optional[Summary] = Relationship(back_populates="highlights")
