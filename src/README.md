## Models

Backend is written in Python. Its uses [FastAPI](https://fastapi.tiangolo.com/) to server two simple endpoints. One to return the highlights and the other to return the key summary.

Extractive summary uses word embeddings (Glove) and get the cosine similarity of the sentences. It then ranks (textrank) the sentences based on the similarity.

### Developement

Install the dependencies
```
python3 -m venv venv
python3 install -r requirements.txt
```

Download stopword and sentence tokenizer data from `nltk`
```
python3 -m nltk.downloader punkt
python3 -m nltk.downloader stopwords
```

Download glove embeddings
```
wget http://nlp.stanford.edu/data/glove.6B.zip -P ./corpus
unzip ./corpus/glove*.zip
```

Run the app
```
python3 app.py
```

Checkout Swagger documentation
```
http://localhost:8000/docs
```
