# Krisp
Browse the web faster with automatic summary.

![Krisp banner](/public/krisp_logo.png)

Krisp is an automatic summary tool to help you browse the web faster. The summary is created using machine learning models. The most important sentences in the article are highlighted using the Textrank algorithm. And the Bert model is used to generate a brief summary.

> Note: It's more of a proof of concept. It uses some heavy computation and not published to chrome web store (yet).

### How it works

Extension uses Readability API to extract the text from the website and forwards it to the backend for extractive and abstractive summary. Extractive summary gets highlighted on the page and the abstractive summary shows in the sidebar.

The Krisp browser extension lives inside ./extension in this repositoty. Whereas the backend lives inside ./src folder.

### Demo

* `Ctrl + Shift + S` -- Linux
* `Cmd + Shift + S` -- Mac Os

![Krisp Workflow](/public/workflow.gif)


Now, it also comes with the **Reader Mode**
Before             |  After
:-------------------------:|:-------------------------:
![](/public/before_reader_mode.png)  |  ![](/public/after_reader_mode.png)
### How to run locally


**Google Chrome**

* Clone the repo `git clone https://github.com/RohitAg13/krisp`.
* In Chrome go to the extensions page (chrome://extensions).
* Enable Developer Mode.
* Drag the `./extension` folder anywhere on the page to import it (do not delete the folder afterwards).


**Backend**

Checkout detailed Docs [here](/src/)


## Licence

> [MIT licence](./LICENSE)
