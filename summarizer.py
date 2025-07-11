from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import re

# Load model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Split long text into manageable chunks
def split_text(text, max_words=800):
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

# Summarization logic using BART with optimized settings
def summarize_text(text):
    chunks = split_text(text)
    summaries = []

    for chunk in chunks:
        inputs = tokenizer.encode(chunk, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs,
            do_sample=True,             # Faster sampling instead of beam search
            top_k=50,                   # Limits vocab for sampling
            top_p=0.95,                 # Nucleus sampling
            max_length=420,             # Desired output length
            min_length=200,             # Minimum summary length
            no_repeat_ngram_size=3      # Avoid repeated phrases
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    return "\n\n".join(summaries)
