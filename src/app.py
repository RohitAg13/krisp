import time
from typing import Optional

import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logger import create_logger
from models.textrank import get_summary as textrank_summary
from models.transformer import get_summary as transformer_summary
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging = create_logger(__name__)


class SummaryRequest(BaseModel):
    text: str
    url: Optional[str] = None


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Process-Time: {process_time}")
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health")
async def health_check():
    return {"success": True}


@app.post("/summary/extract")
async def endpoint_extractive_summary(data: SummaryRequest):
    return textrank_summary(data.text)


@app.post("/summary/abstract")
async def endpoint_abstractive_summary(data: SummaryRequest):
    return transformer_summary(data.text)


if __name__ == "__main__":
    uvicorn.run(app)
