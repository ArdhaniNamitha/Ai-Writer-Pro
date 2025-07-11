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
    sentences = re.split(r'(?<=[.!?])\s+', summary_text)
    chunks = []
    current_chunk = []

    for i, sentence in enumerate(sentences):
        if sentence.strip():
            current_chunk.append(sentence.strip())
        if len(current_chunk) >= 4 or i == len(sentences) - 1:
            chunks.append(current_chunk)
            current_chunk = []

    section_titles = [
        "📘 Introduction",
        "🔍 Key Highlights",
        "📌 Important Details",
        "🧭 Insights & Observations",
        "📤 Conclusion",
        "📝 Final Thoughts"
    ]

    output = ""
    for i, chunk in enumerate(chunks):
        heading = section_titles[i % len(section_titles)]
        output += f"\n\n### {heading}\n\n"
        for sentence in chunk:
            output += f"- {sentence.rstrip('.')}\n"

    return output.strip()
