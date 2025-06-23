# spam_checker.py
from inference import preprocess_text, model_rf, vectorizer

def predict_spam_probability(text: str) -> float:
    cleaned = preprocess_text(text)
    tfidf = vectorizer.transform([cleaned])
    prob = model_rf.predict_proba(tfidf)[0][1]  # Probabilitas kelas Spam
    return prob
