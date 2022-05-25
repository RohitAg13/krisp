import json
from functools import partial
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests

from logger import create_logger
from models.config import ModelSetting
from plugins import youtube
from request_models import AbstractiveSummaryResponse, SummaryRequest
from transformers import pipeline

# Available models:
# Pegasus: google/pegasus-large
# mT5: sebuetnlp/mT5_multilingual_XLSum
# BART: sshleifer/distilbart-cnn-12-6
logging = create_logger(__name__)
settings = ModelSetting()
MODEL = "sshleifer/distilbart-cnn-12-6"


def hugging_face_api_inference(
    payload: str, model_name: str
) -> Optional[List[Dict[str, str]]]:
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {settings.hugging_face_api_key}"}
    data = json.dumps(payload)
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code != 200:
        return None
    return response.json()


if settings.hugging_face_api_key:
    summarizer = partial(hugging_face_api_inference, model_name=MODEL)
else:
    summarizer = pipeline(
        "summarization",
        model=MODEL,
        max_length=1024,
        truncation=True,
    )


def get_summary(data: SummaryRequest) -> AbstractiveSummaryResponse:

    # get transcript if the url belongs to youtube video
    url = urlparse(data.url)
    if url.netloc == "www.youtube.com" and url.path == "/watch":
        data.text = youtube.get_transcript(data.url)

    logging.info(f"length of text: {len(data.text)} words")

    if not len(data.text):
        return AbstractiveSummaryResponse(success=False, summary="")

    summarized = summarizer(
        data.text,
    )
    summary = summarized[0]["summary_text"] if summarized else ""
    logging.info(f"length of summary: {len(summary)} sentences")
    return AbstractiveSummaryResponse(success=len(summary) > 0, summary=summary)


if __name__ == "__main__":
    # sanity test
    text = """Over the past few years as smartphone penetration boomed, products matured, product design and user experience matured, people's expectations have increased.
No longer does a quickly thrown together prototype cut it. People expect a minimum level of good UX and ease-of-use, else they'll leave your app before even giving it a proper try.
In fact, in 2022 great UX might be one strong reason people pick your product over incumbents. That's what happened with Transistor.fm, who made podcast hosting simple and easy.
People expect good aesthetics that make a first impression, simply because that's what they have become used to from the plethora of beautiful and well-designed apps out there in the world.
People expect products to be fully functional as advertised. Buggy products are not acceptable, and in fact people might quickly take to Twitter or social media to let others know that a product is unreliable.
The MVP mindset intensely focuses on building the bare minimum, and that often leaves users frustrated and drives them to seek alternative solutions. Stiffer competition means that people WILL compare your product to alternatives in the market, it's inevitable. And unless you provide something unique and valuable that nobody else does, people are likely to leave.
All these reasons and more make MVP a dated concept, especially in the context of SaaS products. But above all, I think the MVP mindset makes product builders think too heavily about the "minimum" and often so at the cost of "viable".
That's a common pitfall and to avoid that, I propose the MLP framework."""
    result = get_summary(text)
    assert isinstance(result, AbstractiveSummaryResponse)
    summary = result.summary
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert summary not in text
