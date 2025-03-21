from transformers import pipeline

# Summarizer pipeline
summarizer = pipeline("summarization", model="t5-small", device=-1)

# Function to summarize text
def summarize_text(text):
    if len(text) < 10:
        return text  # Return the original text if it's too short for summarization

    truncated_text = text[:500]  # Prevents exceeding model limits
    
    # Adjust lengths dynamically
    max_len = min(100, len(truncated_text) // 2)  # Ensuring max_length is reasonable
    min_len = max(10, max_len // 3)  # Keeping min_length valid

    summary = summarizer(f"summarize: {truncated_text}", max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']
