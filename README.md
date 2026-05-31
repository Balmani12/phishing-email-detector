# 🎣 Phishing Email Detector

A Machine Learning based phishing email detection system built with Python and Scikit-learn that classifies emails as **Phishing** or **Safe** using TF-IDF vectorization and Random Forest classification with custom feature engineering.

---

## 📌 About

This tool was built to demonstrate real-world email security concepts including machine learning based threat detection, natural language processing, and behavioral feature analysis — key concepts in cybersecurity and threat intelligence.

---

## ✨ Features

- ✅ **ML Model** — Random Forest Classifier with 100 estimators
- ✅ **TF-IDF Vectorization** — Text feature extraction with bigrams
- ✅ **Custom Feature Engineering** — 7 hand-crafted security features
- ✅ **Confidence Score** — Shows Safe % and Phishing % probability
- ✅ **Confusion Matrix** — Visual model performance evaluation
- ✅ **Feature Importance Chart** — Shows which features matter most
- ✅ **Suspicious URL Detection** — Detects malicious domains (.xyz, .tk, bit.ly)
- ✅ **Urgency Word Detection** — Flags social engineering keywords
- ✅ **Live Email Checker** — Interactive real-time prediction tool
- ✅ **Sender Spoofing Detection** — Detects PayPal, Amazon, Google spoofs

---

## 🛠️ Technologies Used

- Python 3
- Scikit-learn (Random Forest, TF-IDF)
- NumPy & Pandas
- Matplotlib (Visualization)
- Regex (Pattern matching)

---

## 🔍 Feature Engineering

| Feature | Description |
|---|---|
| url_count | Number of URLs in email |
| suspicious_url | Detects malicious domains (.xyz, .tk, bit.ly) |
| urgency_words | Count of urgency keywords (urgent, expire, now) |
| caps_ratio | Ratio of uppercase letters |
| exclamations | Number of exclamation marks |
| cred_request | Detects credential requests (password, SSN, bank) |
| sender_spoof | Detects brand spoofing (PayPal, Amazon, Google) |

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/Balmani12/phishing-email-detector

# Navigate to folder
cd phishing-email-detector

# Install dependencies
pip install scikit-learn numpy pandas matplotlib

# Run the detector
python phishing_detector.py
```

---

## 📊 Sample Output

```
============================================
   PHISHING EMAIL DETECTOR - RESULTS
============================================
  Accuracy : 100.0%

Classification Report:
              precision  recall  f1-score
Safe              1.00    1.00      1.00
Phishing          1.00    1.00      1.00

---- Built-in Test Examples ----------------

  Result     : [PHISHING] PHISHING
  Confidence : Safe=2.1%  |  Phishing=97.9%
  Features   : URLs=1  Urgency=1  Exclamations=1

  Result     : [SAFE] SAFE
  Confidence : Safe=96.3%  |  Phishing=3.7%
  Features   : URLs=0  Urgency=0  Exclamations=0
```

---

## 🔐 Security Concepts Covered

- **Phishing Detection** — Identifying social engineering attacks
- **URL Analysis** — Detecting malicious and spoofed domains
- **NLP for Security** — Using text analysis for threat detection
- **Feature Engineering** — Building security-focused ML features
- **Behavioral Analysis** — Urgency, caps, exclamations as attack signals
- **Machine Learning** — Random Forest for classification

---

## 📚 What I Learned

- Building ML models for cybersecurity threat detection
- Natural Language Processing with TF-IDF
- Feature engineering for security applications
- Evaluating model performance with confusion matrix
- Real-world phishing attack patterns and indicators

---

## 👨‍💻 Author

**Balmani**
- 🔗 LinkedIn: [linkedin.com/in/bal-mani-7457a11ba](https://linkedin.com/in/bal-mani-7457a11ba)
- 🐙 GitHub: [github.com/Balmani12](https://github.com/Balmani12)
- 🎯 TryHackMe: [tryhackme.com/p/balmani](https://tryhackme.com/p/balmani)
