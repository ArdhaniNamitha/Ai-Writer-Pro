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
    import re

    # Extract first heading as main title if available
    title_match = re.match(r'^#{1,6}\s+(.*)', summary_text)
    main_title = title_match.group(1).strip() if title_match else "📄 Summary"

    # Split by markdown headings or fallback with sentence grouping
    sections = re.split(r'(#+ .+)', summary_text)
    output = f"## 📄 {main_title}\n"

    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            heading = sections[i].strip()
            body = sections[i+1].strip() if i+1 < len(sections) else ""
            body_lines = [f"- {line.strip().rstrip('.')}" for line in body.split('. ') if line.strip()]
            output += f"\n\n### {heading}\n" + "\n".join(body_lines)
    else:
        # Fallback mode (no headings detected)
        fallback_headings = [
            "📘 Introduction",
            "🔍 Key Takeaways",
            "🧠 Author’s View",
            "📌 Examples & Insights",
            "📤 Conclusion",
            "📝 Final Thoughts"
        ]
        sentences = re.split(r'(?<=[.!?])\s+', summary_text)
        chunks, current = [], []
        for i, sentence in enumerate(sentences):
            current.append(sentence.strip())
            if len(current) >= 4 or i == len(sentences) - 1:
                chunks.append(current)
                current = []
        for i, chunk in enumerate(chunks):
            heading = fallback_headings[i % len(fallback_headings)]
            output += f"\n\n### {heading}\n"
            for line in chunk:
                output += f"- {line.rstrip('.')}\n"

    return output.strip()
