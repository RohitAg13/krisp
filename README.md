# Krisp
Browse the web faster with automatic summary.

![Krisp banner](/public/krisp_logo.png)

Krisp is an automatic summary tool which uses two separate methods to get you the summary of almost any article.
It uses Pagerank algorithm to high the key sentences in the article. And uses Bert model to get short summary
of the article.

It is available as a chrome extension that highlights key sentences.
> It uses some heavy computation and not published to chrome web store. It's more of a proof of concept.

### Features

Extension uses Readability API to extract the text from the website and forwards to the backend for extractive and abstractive summary. Extractive summary gets highlighted on the page and the abstractive summary shows as a pop up on the right side.

The Krisp browser extension lives inside ./extension in this repositoty. Whereas the backend lives inside ./src folder.

### How it works

`Ctrl + Shift + S` -- Linux
`Cmd + Shift + S` -- Mac Os

![Krisp Workflow](/public/workflow.gif)

### How to run locally


**Google Chrome**

* Clone the repo `git clone https://github.com/RohitAg13/krisp`.
* In Chrome go to the extensions page (chrome://extensions).
* Enable Developer Mode.
* Drag the `./extension` folder anywhere on the page to import it (do not delete the folder afterwards).


**Backend**

Checkout detailed Docs [here](/src/README.md)
