from fastapi import Depends
from sqlmodel import Session, select

from database.models import Highlight, Summary
from request_models import (
    AbstractiveSummaryResponse,
    BaseSummaryResponse,
    ExtractSummaryResponse,
)


def create_summary(data: BaseSummaryResponse, summary_type: str, session: Session):
    summary = Summary(
        url=data.url,
        summary_type=summary_type,
        word_count=data.word_count,
        summary_word_count=data.summary_word_count,
        response_time=data.response_time,
    )
    session.add(summary)
    if summary_type == "abstractive":
        summary.summary = data.summary
    else:
        for highlight in data.highlights:
            session.add(Highlight(highlight=highlight, summary_id=summary.id))
    session.commit()
    session.refresh(summary)
    return summary


def log_abstractive_summary(data: AbstractiveSummaryResponse, session: Session):
    summary = Summary(
        url=data.url,
        summary_type="abstractive",
        highlight=None,
        summary=data.summary,
        word_count=data.word_count,
        summary_word_count=data.summary_word_count,
        response_time=data.response_time,
    )
    session.add(summary)
    session.commit()
    return summary


def log_extractive_summary(data: ExtractSummaryResponse, session: Session):
    summary = Summary(
        url=data.url,
        summary_type="extractive",
        summary=None,
        word_count=data.word_count,
        summary_word_count=data.summary_word_count,
        response_time=data.response_time,
    )
    for highlight in data.highlights:
        session.add(Highlight(highlight=highlight, summary=summary))
    session.commit()
    return summary


def select_summary(url: str, session: Session):
    statement = select(Summary).where(Summary.url == url)
    result = session.exec(statement)
    summary = result.first()
    return summary
