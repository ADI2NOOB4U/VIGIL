const TRUSTED_SITES = [
  "google.com",
  "amazon.in",
  "amazon.com",
  "github.com",
  "claude.ai",
  "chat.openai.com",
  "youtube.com",
  "linkedin.com",
  "microsoft.com",
  "apple.com"
];

// 🔹 Check trusted domains
function isTrusted(url) {
  return TRUSTED_SITES.some(site => url.includes(site));
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {

    // ✅ SKIP TRUSTED SITES
    if (isTrusted(tab.url)) {
      console.log("✅ Trusted site, skipping:", tab.url);

      chrome.action.setBadgeText({
        text: "SAFE",
        tabId: tabId
      });

      chrome.action.setBadgeBackgroundColor({
        color: "green",
        tabId: tabId
      });

      return;
    }

    console.log("🔍 Scanning:", tab.url);

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

      // 🚨 BLOCK ONLY IF VERY HIGH RISK
      if (percent >= 85) {
        console.log("🚨 Blocking phishing site:", tab.url);

        chrome.tabs.update(tabId, {
          url: chrome.runtime.getURL("blocked.html")
        });
      }
    })
    .catch(err => console.log("❌ Error:", err));
  }
});