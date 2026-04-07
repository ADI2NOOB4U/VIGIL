# 🛡️ Vigil Is Online  
## Project Report – Phishing Detection & Browser Protection System

---

## 1. 📌 Abstract

Phishing attacks are among the most common and dangerous cybersecurity threats, tricking users into revealing sensitive information through malicious websites.  

**Vigil Is Online** is a real-time phishing detection system that leverages machine learning and browser integration to identify and block suspicious URLs before users interact with them.  

The system combines **feature extraction**, a **trained classification model**, and a **browser extension** to provide seamless and proactive protection.

---

## 2. 🎯 Problem Statement

With the rapid growth of online services, phishing attacks have become increasingly sophisticated.  

Traditional detection methods:
- Often rely on blacklists (ineffective for new attacks)  
- Lack real-time adaptability  
- Require manual reporting  

There is a need for an **automated, intelligent, and real-time solution** that can:
- Detect unseen phishing URLs  
- Protect users during browsing  
- Provide immediate feedback  

---

## 3. 💡 Proposed Solution

**Vigil Is Online** addresses this problem using:

- 🧠 **Machine Learning Model** trained on phishing & legitimate URLs  
- 🔍 **Feature Extraction Engine** to analyze URL characteristics  
- 🌐 **Browser Extension** for real-time monitoring  
- 🚫 **Blocking Mechanism** to prevent access to malicious sites  

The system works instantly when a user visits a URL, ensuring proactive protection.

---

## 4. ⚙️ System Architecture

```mermaid
flowchart LR
A[User Visits URL] --> B[Feature Extraction]
B --> C[ML Model]
C --> D{Classification}
D -->|Legitimate| E[Allow Access]
D -->|Phishing| F[Block & Warn]
