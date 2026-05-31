# =============================================
# PHISHING EMAIL DETECTOR - Scikit-learn Model
# Run: python phishing_detector.py
# =============================================

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                              confusion_matrix, ConfusionMatrixDisplay)
import matplotlib.pyplot as plt
import re, warnings
warnings.filterwarnings('ignore')

# ── 1. DATASET ────────────────────────────────
emails = [
    # PHISHING emails
    ("URGENT! Your account is suspended. Click http://paypa1-secure.xyz/verify now or lose access PERMANENTLY!", 1),
    ("You won $1,000,000! Claim prize at http://bit.ly/free-prize Send SSN and bank details immediately!", 1),
    ("ALERT: Suspicious login detected. Verify password at http://amaz0n-login.tk/secure WITHIN 24 HOURS!", 1),
    ("Dear customer, your PayPal is LIMITED. Go to http://secure-paypal.xyz and enter credit card NOW!", 1),
    ("Final warning! Account will be DELETED. Confirm identity: http://apple-id-verify.ru/login URGENT!", 1),
    ("Congratulations! You are selected winner. Send $200 processing fee to claim $500,000 lottery prize!", 1),
    ("Your Netflix subscription EXPIRED. Update payment at http://netflix-billing.xyz or lose access TODAY!", 1),
    ("Bank account compromised! Call +1-800-FAKE-NUM immediately and provide your account number and PIN!", 1),
    ("Microsoft Security Alert: Virus detected! Call support now. Do NOT turn off computer. Click here!", 1),
    ("IRS TAX REFUND: You are owed $3,240. Verify SSN at http://irs-refund.tk to receive money IMMEDIATELY!", 1),
    ("Your DHL package held! Pay customs fee $2.99 at http://dhl-customs.xyz/pay or parcel returned!", 1),
    ("WINNER WINNER! Your email won the UK lottery 850,000 pounds! Send passport copy to claim@lottery.tk NOW!", 1),
    ("Verify your Google account or it will be deleted! Click http://google-verify.xyz/signin urgently!", 1),
    ("Your salary increment approved! Provide bank account to hr-dept@company-payroll.xyz for transfer!", 1),
    ("FINAL NOTICE from Social Security Admin: SSN suspended for fraud. Call 1-800-XXX-XXXX IMMEDIATELY!", 1),

    # SAFE emails
    ("Hi team, the sprint planning meeting is scheduled for Monday at 10 AM. Please review the backlog beforehand.", 0),
    ("Your order #12345 has been shipped. Expected delivery is Thursday. Track at amazon.com/orders.", 0),
    ("Monthly newsletter: Top 5 Python libraries to learn in 2026. Unsubscribe anytime at techblog.com.", 0),
    ("Reminder: Your dentist appointment is confirmed for Friday June 2nd at 3:00 PM. Reply to reschedule.", 0),
    ("Your GitHub pull request was reviewed. Two comments added. Please check the inline suggestions.", 0),
    ("Hi John, great catching up yesterday! Attaching the project proposal we discussed. Let me know thoughts.", 0),
    ("Your Spotify Premium renews on June 15 for Rs 119. Manage subscription at spotify.com/account.", 0),
    ("Q1 earnings report is ready for review. Please find the attached PDF and share feedback by Friday.", 0),
    ("Welcome to the team! Your onboarding schedule and laptop setup guide are linked in this email.", 0),
    ("Stack Overflow weekly digest: Top questions this week in Python, JavaScript and machine learning.", 0),
    ("Your flight booking is confirmed. Check-in opens 24 hours before departure at indigo.com.", 0),
    ("Meeting notes from yesterday's standup attached. Action items assigned to respective owners.", 0),
    ("Code review request: Please review PR #89 for the new authentication module by end of day.", 0),
    ("Your library book is due in 3 days. Renew online at library.org or return to avoid late fees.", 0),
    ("Happy Birthday! Wishing you a wonderful day. Let us know if you want to celebrate with the team!", 0),
]

# ── 2. FEATURE ENGINEERING ────────────────────
def extract_features(text):
    features = {}
    features['url_count']      = len(re.findall(r'http[s]?://\S+', text))
    features['suspicious_url'] = int(bool(re.search(r'bit\.ly|\.xyz|\.tk|\.ru|\d{1,3}\.\d{1,3}', text)))
    features['urgency_words']  = sum(text.lower().count(w) for w in
                                     ['urgent','immediately','expire','suspended',
                                      'warning','final','now','today'])
    features['caps_ratio']     = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    features['exclamations']   = text.count('!')
    features['cred_request']   = int(bool(re.search(r'password|ssn|credit card|bank account|passport', text.lower())))
    features['sender_spoof']   = int(bool(re.search(r'paypa[l1]|amaz[o0]n|g[o0]{2}gle|app[l1]e', text.lower())))
    return features

df = pd.DataFrame([{'text': e[0], 'label': e[1], **extract_features(e[0])} for e in emails])

feature_cols = ['url_count','suspicious_url','urgency_words',
                'caps_ratio','exclamations','cred_request','sender_spoof']

X_text  = df['text']
X_feats = df[feature_cols].values
y       = df['label']

# ── 3. TRAIN / TEST SPLIT ─────────────────────
X_text_tr, X_text_te, X_feat_tr, X_feat_te, y_tr, y_te = train_test_split(
    X_text, X_feats, y, test_size=0.25, random_state=42)

# ── 4. TF-IDF + COMBINED FEATURES ─────────────
tfidf = TfidfVectorizer(max_features=500, ngram_range=(1,2), stop_words='english')
X_tr_tfidf = tfidf.fit_transform(X_text_tr).toarray()
X_te_tfidf = tfidf.transform(X_text_te).toarray()

X_train = np.hstack([X_tr_tfidf, X_feat_tr])
X_test  = np.hstack([X_te_tfidf, X_feat_te])

# ── 5. TRAIN MODEL ────────────────────────────
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_tr)

# ── 6. EVALUATE ───────────────────────────────
y_pred = model.predict(X_test)
acc = accuracy_score(y_te, y_pred)

print("\n============================================")
print("   PHISHING EMAIL DETECTOR - RESULTS")
print("============================================")
print(f"  Accuracy : {acc*100:.1f}%")
print("\nClassification Report:")
print(classification_report(y_te, y_pred, target_names=['Safe','Phishing']))

# ── 7. CONFUSION MATRIX + FEATURE IMPORTANCE PLOT ──
cm = confusion_matrix(y_te, y_pred)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Safe','Phishing'])
disp.plot(ax=axes[0], colorbar=False, cmap='Blues')
axes[0].set_title('Confusion Matrix', fontweight='bold')

feat_imp = model.feature_importances_[-7:]
axes[1].barh(feature_cols, feat_imp, color='#58a6ff')
axes[1].set_title('Feature Importance', fontweight='bold')
axes[1].set_xlabel('Importance Score')

plt.tight_layout()
plt.savefig('results.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n  Chart saved as results.png")

# ── 8. PREDICT FUNCTION ───────────────────────
def predict_email(text):
    feats = np.array([[*extract_features(text).values()]])
    tfidf_vec = tfidf.transform([text]).toarray()
    combined = np.hstack([tfidf_vec, feats])
    pred = model.predict(combined)[0]
    prob = model.predict_proba(combined)[0]
    label = "PHISHING" if pred == 1 else "SAFE"
    print(f"\n  Result     : {'[PHISHING]' if pred==1 else '[SAFE]'} {label}")
    print(f"  Confidence : Safe={prob[0]*100:.1f}%  |  Phishing={prob[1]*100:.1f}%")
    print(f"  Features   : URLs={extract_features(text)['url_count']}  "
          f"Urgency={extract_features(text)['urgency_words']}  "
          f"Exclamations={extract_features(text)['exclamations']}")

# ── 9. BUILT-IN TEST EXAMPLES ─────────────────
print("\n---- Built-in Test Examples ----------------")
predict_email("URGENT! Click http://paypal-secure.xyz now to verify your account!")
predict_email("Hi, the team lunch is at 1 PM today at the usual place. See you there!")

# ── 10. INTERACTIVE USER INPUT LOOP ──────────
print("\n" + "="*50)
print("  LIVE EMAIL CHECKER")
print("  Paste any email below to check if it is")
print("  Phishing or Safe.")
print("  Type 'quit' to exit.")
print("="*50)

while True:
    print("\nPaste your email content below.")
    print("When done, type END on a new line:")
    print("-" * 40)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        if line.strip().lower() == "quit":
            lines = ["quit"]
            break
        lines.append(line)

    user_email = "\n".join(lines).strip()

    if user_email.lower() == "quit":
        print("\nExiting... Goodbye!")
        break

    if user_email:
        predict_email(user_email)
        print("-" * 40)
    else:
        print("No input detected. Please paste some email content.")