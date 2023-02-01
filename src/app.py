import time

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from database.crud import log_abstractive_summary, log_extractive_summary
from database.db import create_db_and_tables, get_session
from fuzzy_replace import get_highlight
from logger import create_logger
from models.textrank import get_summary as textrank_summary
from models.transformer import get_summary as transformer_summary
from request_models import (
    AbstractiveSummaryResponse,
    ExtractSummaryResponse,
    MarkerRequest,
    MarkerResponse,
    SummaryRequest,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging = create_logger(__name__)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Process-Time: {process_time}")
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
async def health_check():
    return {"success": True}


@app.post("/apply-marker")
async def endpoint_apply_marker(data: MarkerRequest) -> MarkerResponse:
    updated_html = get_highlight(data.inner_html, data.summaries)
    return MarkerResponse(inner_html=updated_html)


@app.post("/summary/extract")
async def endpoint_extractive_summary(
    data: SummaryRequest, session: Session = Depends(get_session)
) -> ExtractSummaryResponse:
    response = textrank_summary(data)
    log_extractive_summary(response, session)
    return response


@app.post("/summary/abstract")
async def endpoint_abstractive_summary(
    data: SummaryRequest, session: Session = Depends(get_session)
) -> AbstractiveSummaryResponse:
    response = transformer_summary(data)
    log_abstractive_summary(response, session)
    return response


if __name__ == "__main__":
    uvicorn.run(app)
