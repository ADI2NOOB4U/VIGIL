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

// 🔹 Suspicious TLDs
const SUSPICIOUS_TLDS = [".xyz", ".ml", ".ga", ".cf", ".tk", ".top"];

// 🔹 Extract clean domain
function getDomain(url) {
  try {
    return new URL(url).hostname.replace("www.", "");
  } catch {
    return "";
  }
}

// 🔹 Trusted check (FIXED)
function isTrusted(domain) {
  return TRUSTED_SITES.some(site =>
    domain === site || domain.endsWith("." + site)
  );
}

// 🔹 Suspicious TLD (FIXED)
function hasSuspiciousTLD(domain) {
  return SUSPICIOUS_TLDS.some(tld => domain.endsWith(tld));
}

// 🔥 Fake brand detection (STRONG)
function hasFakeBrand(domain) {
  const brands = ["google", "amazon", "paypal", "microsoft", "apple", "facebook"];

  return brands.some(brand => {
    return domain.includes(brand) &&
      !domain.endsWith(brand + ".com") &&
      !domain.endsWith(brand + ".in") &&
      !domain.endsWith(brand + ".org");
  });
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {

    // ✅ Skip browser internal pages
    if (tab.url.startsWith("chrome://") || tab.url.startsWith("edge://")) return;

    const domain = getDomain(tab.url);

    // ✅ TRUSTED
    if (isTrusted(domain)) {
      chrome.action.setBadgeText({ text: "SAFE", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "green", tabId });
      console.log("✅ Trusted:", domain);
      return;
    }

    console.log("🔍 Scanning:", domain);

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

      chrome.action.setBadgeText({ text: percent.toString(), tabId });
      chrome.action.setBadgeBackgroundColor({
        color: percent >= 70 ? "red" : percent >= 40 ? "yellow" : "green",
        tabId
      });

      console.log(`📊 ${domain} → ${percent}%`);

      const suspiciousTLD = hasSuspiciousTLD(domain);
      const fakeBrand = hasFakeBrand(domain);

      // =========================
      // 🚨 HARD RULES (TOP PRIORITY)
      // =========================

      // 🔥 .com. trick (100% phishing)
      if (domain.includes(".com.") || domain.includes(".net.") || domain.includes(".org.")) {
        console.log("🚨 BLOCKED (.com trick):", domain);

        chrome.tabs.update(tabId, {
          url: chrome.runtime.getURL("blocked.html")
        });
        return;
      }

      // 🔥 Fake brand
      if (fakeBrand) {
        console.log("🚨 BLOCKED (Fake brand):", domain);

        chrome.tabs.update(tabId, {
          url: chrome.runtime.getURL("blocked.html")
        });
        return;
      }

      // =========================
      // 🤖 AI + RULE HYBRID
      // =========================

      // High confidence + bad TLD
      if (percent >= 90 && suspiciousTLD) {
        console.log("🚨 BLOCKED (AI + bad TLD):", domain);

        chrome.tabs.update(tabId, {
          url: chrome.runtime.getURL("blocked.html")
        });
      }

      // Only warning
      else if (percent >= 75) {
        console.log("⚠️ Suspicious:", domain);
      }

    })
    .catch(err => console.log("❌ Error:", err));
  }
});