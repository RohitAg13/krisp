from pagerank import run_summarization

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


@app.post("/summarize")
async def endpoint_summarize(text: str = Body(..., embed=True)):
    summary = run_summarization(text)
    return summary


if __name__ == "__main__":
    uvicorn.run(app)
