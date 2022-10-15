from typing import List, Optional

from pydantic import BaseModel


class MarkerRequest(BaseModel):
    inner_html: str
    summaries: List[str]


class SummaryRequest(BaseModel):
    text: str
    url: Optional[str] = None


class ExtractSummaryResponse(BaseModel):
    highlights: List[str]
    apply_highlights: bool = True
    success: bool = True


class AbstractiveSummaryResponse(BaseModel):
    summary: str
    success: bool = True
