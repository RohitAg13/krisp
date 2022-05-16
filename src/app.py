import time

import uvicorn

from abstractive_summary import get_summary as transformer_summary
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pagerank import get_summary as page_rank_summary

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health")
async def health_check():
    return {"success": True}


@app.post("/summary/extract")
async def endpoint_extractive_summary(text: str = Body(..., embed=True)):
    return page_rank_summary(text)


@app.post("/summary/abstract")
async def endpoint_abstractive_summary(text: str = Body(..., embed=True)):
    return transformer_summary(text)


if __name__ == "__main__":
    uvicorn.run(app)
