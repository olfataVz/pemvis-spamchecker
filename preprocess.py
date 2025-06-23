import pandas as pd
import re
import string
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# nltk.download('punkt')
# nltk.download('stopwords')

# Inisialisasi Stemmer dan Stopwords satu kali
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Daftar slangwords untuk normalisasi
slangwords = {
    "grtis": "gratis",
    "klk": "klik",
    "dpt": "dapat",
    "lgsg": "langsung",
    "blm": "belum",
    "udh": "sudah",
    "dgn": "dengan",
    "gk": "tidak",
    "ga": "tidak",
    "tdk": "tidak",
    "td": "tidak",
    "krn": "karena",
    "utk": "untuk",
    "sy": "saya",
    "gw": "saya",
    "aku": "saya",
    "km": "kamu",
    "loe": "kamu",
    "anda": "kamu",
    "dr": "dari",
    "sm": "sama",
    "aja": "saja",
    "nih": "ini",
    "nya": "",
    "trs": "terus",
    "bgt": "banget",
    "bbrp": "beberapa",
    "tp": "tapi",
    "jg": "juga",
    "udh": "sudah",
    "lg": "lagi",
    "krm": "kirim",
    "dpn": "depan",
    "bsk": "besok",
    "mrh": "murah",
    "diskon": "potongan harga",
    "cb": "coba",
    "cek": "periksa",
    "dtg": "datang",
    "brg": "barang",
    "ptg": "penting",
    "no": "nomor"
}

def cleaningText(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Menghapus mention
    text = re.sub(r'#[A-Za-z0-9]+', '', text)  # Menghapus hashtag
    text = re.sub(r'RT[\s]+', '', text)        # Menghapus RT
    text = re.sub(r"http\S+", '', text)        # Menghapus link
    text = re.sub(r'[0-9]+', '', text)          # Menghapus angka
    text = re.sub(r'[^\w\s]', '', text)         # Menghapus karakter selain huruf dan angka
    text = text.replace('\n', ' ')              # Mengganti baris baru dengan spasi
    text = text.translate(str.maketrans('', '', string.punctuation))  # Menghapus tanda baca
    text = text.strip()                         # Menghapus spasi kiri-kanan
    return text

def casefoldingText(text):
    return text.lower()

def fix_slangwords(text):
    words = text.split()
    fixed_words = [slangwords[word.lower()] if word.lower() in slangwords else word for word in words]
    return ' '.join(fixed_words)

def tokenizingText(text):
    return word_tokenize(text)

def stemmingText(text):
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    return ' '.join(stemmed_words)

def toSentence(tokens):
    return ' '.join(tokens)
