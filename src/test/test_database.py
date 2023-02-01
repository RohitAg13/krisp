import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from database.models import Summary, Highlight
from database.crud import (
    create_summary,
    log_abstractive_summary,
    log_extractive_summary,
)
from request_models import ExtractSummaryResponse, AbstractiveSummaryResponse


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_summary(session: Session):
    create_summary(
        data=ExtractSummaryResponse(
            url="https://www.google.com",
            word_count=100,
            summary_word_count=100,
            response_time=100,
            highlights=["This is a highlight"],
        ),
        summary_type="extractive",
        session=session,
    )
    create_summary(
        data=AbstractiveSummaryResponse(
            url="https://www.google.com",
            word_count=100,
            summary_word_count=100,
            response_time=100,
            summary="This is a summary",
        ),
        summary_type="abstractive",
        session=session,
    )


def test_log_abstractive_summary(session: Session):
    summary = log_abstractive_summary(
        data=AbstractiveSummaryResponse(
            url="https://www.google.com",
            summary="This is a summary",
            word_count=100,
            summary_word_count=100,
            response_time=100,
        ),
        session=session,
    )
    assert summary is not None


def test_extractive_summary(session: Session):
    summary = log_extractive_summary(
        data=ExtractSummaryResponse(
            url="https://www.google.com",
            word_count=100,
            summary_word_count=100,
            response_time=100,
            highlights=["This is a highlight"],
        ),
        session=session,
    )
    assert summary is not None
