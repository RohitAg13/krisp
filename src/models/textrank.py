import math
import re
from functools import lru_cache
from time import perf_counter
from typing import List, Tuple
from urllib.parse import urlparse

import networkx as nx
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from numpy.linalg import norm

from logger import create_logger
from plugins import youtube
from request_models import ExtractSummaryResponse, SummaryRequest

logging = create_logger(__name__)
MAX_RESULTS = 15  # maximum number of sentences in the summary
FACTOR = 0.2  # percentage of total sentences to be returned as summary
VECTOR_SIZE = 50  # Size of the Glove vector. Possible values: 50,100,200,300
stop_words = stopwords.words("english")


def remove_stopwords(sentence: List[str]) -> str:
    return " ".join([word for word in sentence if word not in stop_words])


def create_sentences(text: str) -> List[str]:
    # Breaks text into list of sentences.
    return sent_tokenize(text)


def cosine_similarity(A, B):
    return np.dot(A, B) / (norm(A) * norm(B))


def format_sentences(sentences: List[str]) -> List[str]:
    # remove punctuations, numbers and special characters
    clean_sentences = list(map(lambda x: x.replace("[^a-zA-Z]", " "), sentences))
    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]
    # function to remove stopwords
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    return clean_sentences


# Extract word vectors
@lru_cache()
def get_word_embedding(filename: str = f"./corpus/glove.6B.{VECTOR_SIZE}d.txt"):
    word_embeddings = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype="float32")
            word_embeddings[word] = coefs
    return word_embeddings


def create_sentence_embedding(sentences: List[str]) -> List[List[float]]:
    sentence_vectors = []
    word_embeddings = get_word_embedding()
    for i in sentences:
        if len(i) != 0:
            v = sum(
                [word_embeddings.get(w, np.zeros((VECTOR_SIZE,))) for w in i.split()]
            ) / (len(i.split()) + 0.001)
        else:
            v = np.zeros((VECTOR_SIZE,))
        sentence_vectors.append(v)
    return sentence_vectors


def create_similarity_matrix(
    sentences: List[str], sentence_vectors: List[List[float]]
) -> List[List[float]]:
    similarity_matrix = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            similarity_matrix[i][j] = cosine_similarity(
                sentence_vectors[i],
                sentence_vectors[j],
            )
    return similarity_matrix


def rank_sentences(sentences: List[str], similarity_matrix: List[List[float]]):
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank_numpy(nx_graph)
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True
    )
    return ranked_sentences


def remove_non_alphabets(text: str) -> str:
    if not isinstance(text, str):
        print(f"text: {text},\n\n type: {type(text)}")
    return re.sub(r"[^a-zA-Z0-9]", "", text)


def sort_highlight(highlights: List[Tuple[float, str]], text: str) -> List[str]:
    """Sorts highlights based on the order of appearance in the text"""
    # remove extra spaces from text
    text = remove_non_alphabets(text)
    cleaned_highlights = [
        (i, remove_non_alphabets(h[1])) for i, h in enumerate(highlights)
    ]
    cleaned_highlights.sort(key=lambda x: text.find(x[1]))
    sorted_data = [highlights[index] for index, _ in cleaned_highlights]
    return sorted_data


def get_summary(data: SummaryRequest) -> ExtractSummaryResponse:

    # get transcript if the url belongs to youtube video
    start_time = perf_counter()
    is_youtube_link = False
    url = urlparse(data.url)
    if url.netloc == "www.youtube.com" and url.path == "/watch":
        data.text = youtube.get_transcript(data.url)
        is_youtube_link = True

    logging.info(f"length of text: {len(data.text)} words")
    if not len(data.text):
        return ExtractSummaryResponse(
            success=False, highlights=[], apply_highlights=False
        )
    raw_sentences = create_sentences(data.text)
    sentences = format_sentences(raw_sentences)
    sentence_embedding = create_sentence_embedding(sentences=sentences)
    similarity_matrix = create_similarity_matrix(
        sentences=sentences, sentence_vectors=sentence_embedding
    )
    ranked_sentences = rank_sentences(
        sentences=raw_sentences, similarity_matrix=similarity_matrix
    )
    max_sentences = min(MAX_RESULTS, math.ceil(FACTOR * len(sentences)))
    highlights = ranked_sentences[:max_sentences]
    sorted_highlights = sort_highlight(highlights, data.text)
    logging.info(f"length of summary: {len(sorted_highlights)} sentences")
    response_time = perf_counter() - start_time
    return ExtractSummaryResponse(
        url=data.url,
        success=len(sorted_highlights) > 0,
        apply_highlights=not is_youtube_link,
        highlights=[s[1] for s in sorted_highlights],
        word_count=len(data.text),
        summary_word_count=sum([len(s[1]) for s in sorted_highlights]),
        response_time=response_time,
    )


if __name__ == "__main__":
    ## sanity tests
    text = """Over the past few years as smartphone penetration boomed, products matured, product design and user experience matured, people's expectations have increased.
No longer does a quickly thrown together prototype cut it. People expect a minimum level of good UX and ease-of-use, else they'll leave your app before even giving it a proper try.
In fact, in 2022 great UX might be one strong reason people pick your product over incumbents. That's what happened with Transistor.fm, who made podcast hosting simple and easy.
People expect good aesthetics that make a first impression, simply because that's what they have become used to from the plethora of beautiful and well-designed apps out there in the world.
People expect products to be fully functional as advertised. Buggy products are not acceptable, and in fact people might quickly take to Twitter or social media to let others know that a product is unreliable.
The MVP mindset intensely focuses on building the bare minimum, and that often leaves users frustrated and drives them to seek alternative solutions. Stiffer competition means that people WILL compare your product to alternatives in the market, it's inevitable. And unless you provide something unique and valuable that nobody else does, people are likely to leave.
All these reasons and more make MVP a dated concept, especially in the context of SaaS products. But above all, I think the MVP mindset makes product builders think too heavily about the "minimum" and often so at the cost of "viable".
That's a common pitfall and to avoid that, I propose the MLP framework."""
    result = get_summary(SummaryRequest(text=text))
    assert isinstance(result, ExtractSummaryResponse)
    summary = result.highlights
    assert isinstance(summary, list)
    assert len(summary) > 0
    assert isinstance(summary[0], str)
    assert all(s in text for s in summary)
