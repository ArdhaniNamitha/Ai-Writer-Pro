from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import re

# Load BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Split input into chunks
def split_text(text, max_words=600):  # increased chunk size
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    chunk = ""
    word_count = 0
    for sentence in sentences:
        words = sentence.split()
        if word_count + len(words) > max_words:
            chunks.append(chunk.strip())
            chunk = sentence + " "
            word_count = len(words)
        else:
            chunk += sentence + " "
            word_count += len(words)
    if chunk:
        chunks.append(chunk.strip())
    return chunks

# Generate summaries
def summarize_text(text):
    chunks = split_text(text)
    summaries = []
    for chunk in chunks:
        inputs = tokenizer.encode(chunk, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs,
            num_beams=4,
            length_penalty=1.2,      # less aggressive compression
            max_length=300,          # increased from 200
            min_length=100,          # increased from 60
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    return "\n\n".join(summaries)
