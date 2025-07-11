from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import re

# Use faster version of BART
model_name = "sshleifer/distilbart-cnn-12-6"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Split large text into chunks
def split_text(text, max_words=400):
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

# Main summary function (clean, fast, structured)
def summarize_text(text):
    chunks = split_text(text)
    summaries = []

    for chunk in chunks:
        prompt = "Summarize this content with clear section-wise bullet points: " + chunk
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            max_length=300,
            min_length=100,
            no_repeat_ngram_size=3
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    return "\n\n".join(summaries)
