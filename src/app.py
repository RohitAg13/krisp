from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()

ORIGINS = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()


@app.post("/summarize")
async def endpoint_summarize(text: str = Body(...)):
    return text.split(".")


if __name__ == "__main__":
    uvicorn.run(app)
