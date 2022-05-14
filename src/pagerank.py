from typing import List
import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords

# code ported from https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3

MAX_RESULTS = 15
STOPWORD_LANGUAGE = "english"


def create_frequency_table(text_string: str) -> dict:
    stopWords = set(stopwords.words(STOPWORD_LANGUAGE))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable


def create_frequency_matrix(sentences: List[str]) -> dict:
    frequency_matrix = {}
    stopWords = set(stopwords.words(STOPWORD_LANGUAGE))
    ps = PorterStemmer()
    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:MAX_RESULTS]] = freq_table

    return frequency_matrix


def create_tf_matrix(freq_matrix: dict) -> dict:
    tf_matrix = {}
    for sent, f_table in freq_matrix.items():
        tf_table = {}
        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence
        tf_matrix[sent] = tf_table
    return tf_matrix


def create_documents_per_words(freq_matrix: dict) -> dict:
    word_per_doc_table = {}
    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1
    return word_per_doc_table


def create_idf_matrix(
    freq_matrix: dict, count_doc_per_words: dict, total_documents: int
) -> dict:
    idf_matrix = {}
    for sent, f_table in freq_matrix.items():
        idf_table = {}
        for word in f_table.keys():
            idf_table[word] = math.log10(
                total_documents / float(count_doc_per_words[word])
            )
        idf_matrix[sent] = idf_table
    return idf_matrix


def create_tf_idf_matrix(tf_matrix: dict, idf_matrix: dict) -> dict:
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(
        tf_matrix.items(), idf_matrix.items()
    ):
        tf_idf_table = {}
        for (word1, value1), (word2, value2) in zip(
            f_table1.items(), f_table2.items()
        ):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)
        tf_idf_matrix[sent1] = tf_idf_table
    return tf_idf_matrix


def score_sentences(tf_idf_matrix: dict) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    """
    sentenceValue = {}
    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0
        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score
        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence
    return sentenceValue


def find_average_score(sentenceValue: dict) -> int:
    """
    Find the average score from the sentence value dictionary
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]
    # Average value of a sentence from original summary_text
    average = sumValues / len(sentenceValue)
    return average


def generate_summary(
    sentences: List[str], sentenceValue: dict, threshold: float
) -> List[str]:
    sentence_count = 0
    summary = []
    for sentence in sentences:
        if sentence[:MAX_RESULTS] in sentenceValue and sentenceValue[
            sentence[:MAX_RESULTS]
        ] >= (threshold):
            summary.append(sentence)
            sentence_count += 1
    return summary


def run_summarization(text: str) -> List[str]:
    sentences: List[str] = sent_tokenize(text)
    total_documents: int = len(sentences)
    freq_matrix = create_frequency_matrix(sentences)
    tf_matrix = create_tf_matrix(freq_matrix)

    count_doc_per_words = create_documents_per_words(freq_matrix)

    idf_matrix = create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
    tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)

    sentence_scores = score_sentences(tf_idf_matrix)
    threshold = find_average_score(sentence_scores)
    summary = generate_summary(sentences, sentence_scores, 1.3 * threshold)
    return summary
