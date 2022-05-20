const MAX_RESULTS = 20;
const KRISP_ORIGIN = "http://127.0.0.1:8000";
const NON_READABLE_DOMAINS = [
  "www.youtube.com",
  "www.vimeo.com",
  "www.twitch.com",
  "www.twitter.com",
  "www.facebook.com",
  "www.instagram.com",
  "www.reddit.com",
  "www.linkedin.com",
  "www.pinterest.com",
  "www.quora.com",
  "www.flickr.com",
];

async function fetchExtractiveSummary(text) {
  const url = new URL(KRISP_ORIGIN);
  url.pathname = "/summary/extract";
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({ text: text, url: location.href }),
    });
    const result = await resp.json();
    return result;
  } catch (e) {
    console.error(`[krisp] error: could not load similar: ${e}`);
    return { success: false, highlights: [], apply_highlights: false };
  }
}

async function fetchAbstractiveSummary(text) {
  const url = new URL(KRISP_ORIGIN);
  url.pathname = "/summary/abstract";
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({ text: text, url: location.href }),
    });
    const result = await resp.json();
    return result;
  } catch (e) {
    console.error(`[krisp] error: could not load similar: ${e}`);
    return { success: false, summary: "" };
  }
}

function compose({ summary, loading, abstractiveSummary }) {
  return `
      <div class="krisp-root">
          <header>
              <div class="logo"><strong>Krisp</strong> summary</div>
              <button class="closeButton" id="closeButton">×</button>
          </header>
          ${
            loading
              ? `<div class="loading-container">
                  <div class="loading"></div>
              </div>`
              : `<div class="doc-list">
                  <details class="summary" open>
                      <summary>Key Takeaway</summary>
                      ${abstractiveSummary}
                  </details>
                  <details class="summary" close>
                      <summary>Highlights</summary>
                      <ul class="summaryText">
                          ${summary.map((sent) => `<li>${sent}</li>`).join("")}
                      </ul>
                  </details>
              </div>`
          }
      </div>`;
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
  return { textContent: article.textContent, content: article.content };
}

function applyHighlights(summary) {
  for (idx in summary) {
    var text = summary[idx];
    var innerHTML = document.body.innerHTML;
    document.body.innerHTML = innerHTML.replace(
      text,
      "<mark>" + text + "</mark>"
    );
  }
}

chrome.runtime.onMessage.addListener(async (msg) => {
  switch (msg.type) {
    case "search": {
      console.log(`[krisp] received message: ${msg.type}`);

      const { content, textContent } = getPageContent();
      // Reader Mode
      if (!NON_READABLE_DOMAINS.includes(new URL(location.href).hostname)) {
        document.body.innerHTML = `
            <html>
                <style type="text/css">${READER_MODE_STYLES}
                </style>
                <body>${content}
                </body>
            </html>
      `;
      }

      const extractiveSummary = await fetchExtractiveSummary(textContent);

      // highlights
      if (extractiveSummary.apply_highlights) {
        console.log("[krisp] applying highlights");
        applyHighlights(extractiveSummary.highlights);
      }

      // Create shadow container
      const shadowContainer = document.createElement("div");
      shadowContainer.setAttribute("class", "shadow-container");
      const shadowRoot = shadowContainer.attachShadow({ mode: "open" });
      document.body.appendChild(shadowContainer);

      // styles
      const style = document.createElement("style");
      style.textContent = STYLES;
      shadowRoot.appendChild(style);

      // Initialize loader
      var keypoints = compose({
        summary: [],
        loading: true,
        abstractiveSummary: "",
      });
      const node = document.createElement("div");
      node.setAttribute("id", "krisp-container");
      node.innerHTML = keypoints;
      shadowRoot.appendChild(node);

      // Fetch abstractive summary
      console.log("[krisp]: Fetching key takeaways");
      const abstractiveSummary = await fetchAbstractiveSummary(textContent);

      var shadowEle = document.querySelector(
        ".shadow-container:last-of-type"
      ).shadowRoot;

      // Update received summary
      keypoints = compose({
        summary: extractiveSummary.highlights,
        loading: false,
        abstractiveSummary: abstractiveSummary.summary,
      });
      shadowEle.querySelector("#krisp-container").innerHTML = keypoints;

      // close button
      shadowEle
        .querySelector("#closeButton")
        .addEventListener("click", function () {
          shadowEle.querySelector(".krisp-root").remove();
          document.querySelector(".shadow-container").remove();
        });
    }
  }
});
