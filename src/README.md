### Developement

Install the dependencies
```
python3 -m venv venv
python install -r requirements.txt
```

Download stopword and sentence tokenizer data from `nltk`
```
python3 -m nltk.downloader punkt
python3 -m nltk.downloader stopwords
```

Download glove embeddings
```
wget http://nlp.stanford.edu/data/glove.6B.zip
unzip glove*.zip
```

Run the app
```
python3 app.py
```

Checkout Swagger documentation
```
http://localhost:8000/docs
```
