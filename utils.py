import textstat
from docx import Document
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re

def get_readability(text):
    return textstat.flesch_reading_ease(text)

def get_word_count(text):
    return len(text.split())

def extract_text_from_file(file_path, ext):
    text = ""
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

def extract_keywords(text, top_n=5):
    vec = CountVectorizer(stop_words="english", max_features=1000)
    X = vec.fit_transform([text])
    word_freq = np.array(X.sum(axis=0)).flatten()
    keywords = np.array(vec.get_feature_names_out())[word_freq.argsort()[::-1]]
    return keywords[:top_n]

def format_as_study_notes(summary_text):
    import string

    sentences = re.split(r'(?<=[.!?])\s+', summary_text)
    chunks = []
    current_chunk = []

    for i, sentence in enumerate(sentences):
        if sentence.strip():
            current_chunk.append(sentence.strip())
        if len(current_chunk) >= 4 or i == len(sentences) - 1:
            chunks.append(current_chunk)
            current_chunk = []

    fallback_headings = [
        "📘 Introduction",
        "🔍 Key Takeaways",
        "🧠 Author’s View",
        "📌 Examples & Insights",
        "📤 Conclusion",
        "📝 Final Thoughts"
    ]

    used_titles = set()
    output = ""

    for i, chunk in enumerate(chunks):
        heading = None

        # Try to extract a good title from first sentence of the chunk
        first_sentence = chunk[0].strip(string.punctuation)
        words = [w for w in first_sentence.split() if len(w) > 4]

        # Choose best word that's not already used as title
        for word in words:
            word_cap = word.capitalize()
            if word_cap not in used_titles:
                heading = f"### 🧠 {word_cap}"
                used_titles.add(word_cap)
                break

        # Fallback to professional heading list
        if not heading:
            fallback = fallback_headings[i % len(fallback_headings)]
            while fallback in used_titles:
                i += 1
                fallback = fallback_headings[i % len(fallback_headings)]
            heading = f"### {fallback}"
            used_titles.add(fallback)

        # Build section
        output += f"\n\n{heading}\n\n"
        for line in chunk:
            output += f"- {line.rstrip('.')}\n"

    return output.strip()
