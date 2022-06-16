function getItemFromStorage(key) {
  try {
    return chrome.storage.local.get(["key"], function (result) {
      console.log("Value currently is " + result.key);
    });
  } catch (err) {
    console.error(`Error getting item ${key} from localStorage`, err);
    return null;
  }
}

function storeItem(key, value) {
  if (!localStorage) return;
  try {
    return chrome.storage.local.set({ key: value }, function () {
      console.log("Value is set to " + value);
      return value;
    });
  } catch (err) {
    console.error(`Error storing item ${key} to localStorage`, err);
    return null;
  }
}

const enableText = "Disable Abstract Summary";
const disableText = "Enable Abstract Summary";

const isAbstractSummaryEnabled = getItemFromStorage("abstractSummaryEnabled");
var button = document.getElementById("enableAbstractSummary");
button.innerHTML = isAbstractSummaryEnabled ? disableText : enableText;
button.addEventListener("click", function () {
  if (button.innerHTML == enableText) {
    button.innerHTML = disableText;
    storeItem("abstractSummaryEnabled", true);
  } else {
    button.innerHTML = enableText;
    storeItem("abstractSummaryEnabled", false);
  }
});
