### Developement
Install the dependencies
```
python3 -m venv venv
python install -r requirements.txt
```

Download the stopwork and sentence tokenizer data from `nltk`
```
python3 -m nltk.downloader punkt
python3 -m nltk.downloader stopwords
```

Download glove
```
wget http://nlp.stanford.edu/data/glove.6B.zip
unzip glove*.zip
```
