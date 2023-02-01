## Models

Backend is written in Python. Its uses [FastAPI](https://fastapi.tiangolo.com/) to server two simple endpoints. One to return the highlights and the other to return the key summary.

Extractive summary uses word embeddings (Glove) and get the cosine similarity of the sentences. It then ranks (textrank) the sentences based on the similarity.

For Abstractive summary we are using huggingface's Summarization model. For quick accelerated inference [Inference API](https://huggingface.co/inference-api) for

You will need to signup to  hugging face inference API and generate an access token. Paste the access token in `.env` file

### Developement

Install the dependencies

> python.__version__ = 3.7.6
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

On Mac, tokenizer build might fail and require you to install Rust, 
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Download stopword and sentence tokenizer data from `nltk`
```
python3 -c "import nltk; nltk.download('punkt')"
python3 -c "import nltk; nltk.download('stopwords')"
```

Download glove embeddings
```
wget http://nlp.stanford.edu/data/glove.6B.zip -P ./corpus
unzip ./corpus/glove*.zip ./corpus
```

Run the app
```
python3 app.py
```

Checkout Swagger documentation
```
http://localhost:8000/docs
```

## Test

```
python3 -m pytest test
```


## Deploy

Deployment is managed by systemd. Copy the `krisp.service` file to `/etc/systemd/system/krisp.service` and update:

* create user `adduser krisp-user`
* add user to sudoers `usermod -aG sudo krisp-user`
* replace `krisp-user` with your Linux user
* replace `/home/krisp-user/krisp with your working directory

Then start Krisp as a service:

```
systemctl daemon-reload # reload systemd script
systemctl start krisp   # start Krisp server as a service
```
