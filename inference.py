# %%
# inference.py
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from preprocess import cleaningText, casefoldingText, fix_slangwords, tokenizingText, toSentence
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Contoh data uji
test_samples = {
    "1": "GRATIS pulsa 100rb hanya hari ini! Klik link ini sekarang dan klaim hadiahnya: bit.ly/pulsagratis",
    "2": "Selamat !! Anda terpilih mendapatkan hadiah undian motor Honda! Segera hubungi admin kami di WA 081234567890 sebelum hadiah ini hangus.",
    "3": "Halo, besok kita jadi rapat jam 10 pagi ya. Jangan lupa bawa dokumen proposalnya.",
    "4": "Terima kasih atas bantuannya kemarin kawan, besok kita makan mie ayam yok."
}

# 2. Preprocessing sama seperti training
def preprocess_text(text):
    text = cleaningText(text)
    text = casefoldingText(text)
    text = fix_slangwords(text)
    tokens = tokenizingText(text)
    text = toSentence(tokens)
    return text


# %%
# Load model dan tokenizer

with open("saved_model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("saved_model/spam_classifier_model_RF.pkl", "rb") as f:
    model_rf = pickle.load(f)

with open('saved_model/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# %%
# Tentukan max_len sesuai training
max_len = 100  

# Preprocessing semua sample
processed_texts = [preprocess_text(text) for text in test_samples.values()]

# Untuk Random Forest: transform ke TF-IDF
test_tfidf = vectorizer.transform(processed_texts)

# Preprocessing semua sample
processed_texts = [preprocess_text(text) for text in test_samples.values()]

# Untuk LSTM: tokenisasi dan padding
test_seq = tokenizer.texts_to_sequences(processed_texts)
test_pad = pad_sequences(test_seq, maxlen=max_len)

# Prediksi dengan model
predictions_rf = model_rf.predict(test_tfidf)


# %%
probs_rf = model_rf.predict_proba(test_tfidf)  

# print("Hasil prediksi dengan RF:")
# for i, (original_text, prob) in enumerate(zip(test_samples.values(), probs_rf)):
#     label = "Spam" if prob[1] > 0.5 else "Ham"
#     print(f"Teks {i+1}:\n{original_text}\nPrediksi: {label} (prob Spam: {prob[1]:.4f})\n")
