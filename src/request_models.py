from typing import List, Optional

from pydantic import BaseModel


class SummaryData(BaseModel):
    url: str
    summary: str
    highlights: List[str]
    extract_response_time: float
    abstract_response_time: float


class MarkerRequest(BaseModel):
    inner_html: str
    summaries: List[str]


class MarkerResponse(BaseModel):
    inner_html: str


class SummaryRequest(BaseModel):
    text: str
    url: Optional[str] = None


class BaseSummaryResponse(BaseModel):
    url: str = None
    success: bool = True
    word_count: int = 0
    summary_word_count: int = 0
    response_time: float = 0.0


class ExtractSummaryResponse(BaseSummaryResponse):
    highlights: List[str]
    apply_highlights: bool = True


class AbstractiveSummaryResponse(BaseSummaryResponse):
    summary: str
