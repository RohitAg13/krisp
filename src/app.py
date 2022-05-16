from pagerank import get_summary
from abstractive_summary import summarize

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"success": True}


@app.post("/summary/extract")
async def endpoint_extractive_summary(text: str = Body(..., embed=True)):
    summary = get_summary(text)
    return summary


@app.post("/summary/abstract")
async def endpoint_abstractive_summary(text: str = Body(..., embed=True)):
    return summarize(text)


if __name__ == "__main__":
    uvicorn.run(app)
