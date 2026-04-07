chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {

    fetch("http://127.0.0.1:5000/scan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      const percent = Math.round(data.confidence * 100);

      chrome.action.setBadgeText({
        text: percent.toString(),
        tabId: tabId
      });

      chrome.action.setBadgeBackgroundColor({
        color: percent >= 70 ? "red" : percent >= 40 ? "yellow" : "green",
        tabId: tabId
      });

      if (percent >= 70) {
        chrome.tabs.update(tabId, {
          url: chrome.runtime.getURL("blocked.html")
        });
      }
    })
    .catch(err => console.log("Error:", err));
  }
});