import numpy as np
from numpy import ndarray
from models.textrank import (
    remove_stopwords,
    create_sentences,
    get_word_embedding,
    create_sentence_embedding,
    create_similarity_matrix,
    rank_sentences,
    remove_non_alphabets,
    cosine_similarity,
)


def test_remove_stopwords():
    sentence = "This is a sample sentence, showing off the stop words filtration."
    result = remove_stopwords(sentence.split())
    print(f"results: {result}")
    assert result == "This sample sentence, showing stop words filtration."


def test_create_sentences():
    text = "This is a sample sentence. This is another sample sentence."
    assert create_sentences(text) == [
        "This is a sample sentence.",
        "This is another sample sentence.",
    ]


def test_get_word_embedding():
    word_embeddings = get_word_embedding()
    assert len(word_embeddings) > 0


def test_create_sentence_embedding():
    sentences = ["This is a sample sentence.", "This is another sample sentence."]
    sentence_vectors = create_sentence_embedding(sentences)
    assert len(sentence_vectors) == len(sentences)
    assert isinstance(sentence_vectors, list)
    assert isinstance(sentence_vectors[0][0], float)


def test_create_similarity_matrix():
    sentences = ["This is a sample sentence.", "This is another sample sentence."]
    sentence_vectors = create_sentence_embedding(sentences)
    similarity_matrix = create_similarity_matrix(sentences, sentence_vectors)
    assert len(similarity_matrix) == len(sentences)


def test_cosine_similarity():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    cs = cosine_similarity(a, b)
    assert len(cs) == len(a)
