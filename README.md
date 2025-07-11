---
title: AI Writer Pro
emoji: 🧠
colorFrom: pink
colorTo: indigo
sdk: streamlit
app_file: app.py
pinned: false
license: mit
---

# AI Writer Pro

**AI Writer Pro** is a powerful, customizable text summarization and productivity application designed for students, researchers, and professionals. It utilizes advanced NLP models (like BART and T5) to generate high-quality summaries, smart study notes, and extract keywords from various document types (PDF, DOCX, TXT).

## Features

* **Text Summarization**: Generate concise or detailed summaries using state-of-the-art transformer models.
* **Smart Notes Mode**: Automatically formats summaries into structured bullet points for study or review.
* **File Support**: Upload and summarize text from `.pdf`, `.docx`, and `.txt` files.
* **Keyword Extraction**: Extracts top relevant keywords for quick insights.
* **Readability Score**: Calculates Flesch Reading Ease to estimate text difficulty.
* **Responsive UI with Theme Toggle**: Users can switch between light and dark modes for comfortable viewing.
* **Downloadable Output**: Easily download the generated summary for offline use.

## Technologies Used

* **Frontend & Deployment**: Streamlit (deployed on Hugging Face Spaces)
* **Backend Models**: Hugging Face Transformers (`t5-base` or `facebook/bart-large-cnn`)
* **Text Processing**: `nltk`, `textstat`, `sklearn`
* **File Handling**: `pdfplumber`, `python-docx`

## Folder Structure

```

ai\_writer\_pro\_streamlit/
│
├── app.py               # Main Streamlit app logic
├── summarizer.py        # Summarization logic using T5/BART
├── utils.py             # Text extraction, readability, keyword tools
├── requirements.txt     # Dependencies
├── README.md            # Project documentation

```

## How to Run Locally

1. **Clone the repository**:

```

git clone [https://github.com/ArdhaniNamitha/Ai-Writer-Pro.git](https://github.com/ArdhaniNamitha/Ai-Writer-Pro.git)
cd Ai-Writer-Pro

```

2. **Install the dependencies**:

```

pip install -r requirements.txt

```

3. **Launch the Streamlit app**:

```

streamlit run app.py

```

## Deployment

The application is deployed using **Hugging Face Spaces** for persistent and public access. It leverages the Streamlit SDK for an interactive UI and supports continuous updates via Git integration.

## Use Cases

* Summarizing research papers  
* Creating notes from lengthy textbooks  
* Quickly understanding reports and articles  
* Assisting content writers and educators in creating condensed material

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

* Hugging Face Transformers  
* Streamlit Community  
* Open Source Contributors
