async function summarize(text) {
  const url = new URL("http://localhost:8000/summarize");
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({ text: text }),
    });
    const docs = await resp.json();
    return docs.results;
  } catch (e) {
    console.error(`[krisp] error: could not load similar: ${e}`);
    return [];
  }
}

function getPageContent() {
  const selection = window.getSelection().toString().trim();
  if (selection) {
    return selection;
  }
  const readability = new Readability(document.cloneNode(true), {
    charThreshold: 20,
  });
  const article = readability.parse();
  return article.textContent;
}

function applyHighlights(summary) {
  // highlights
  for (idx in summary) {
    var text = summary[idx];
    var innerHTML = document.body.innerHTML;
    var index = innerHTML.indexOf(text);
    if (index >= 0) {
      updatedInnerHTML =
        innerHTML.substring(0, index) +
        "<mark>" +
        innerHTML.substring(index, index + text.length) +
        "</mark>" +
        innerHTML.substring(index + text.length);
      document.body.innerHTML = updatedInnerHTML;
    } else {
      console.log("[krisp]: couldn't find summary in body");
    }
  }
}

chrome.runtime.onMessage.addListener(async (msg) => {
  switch (msg.type) {
    case "search": {
      console.log(`[krisp] received message: ${msg.type}`);
      const content = getPageContent();
      const summaries = await summarize(content);
      applyHighlights(summaries);
    }
  }
});
