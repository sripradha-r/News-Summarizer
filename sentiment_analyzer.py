from transformers import pipeline

# Sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=r"D:\fine_tuned_sentiment_model\fine_tuned_sentiment_model", device=-1)

# Sentiment label mapping
sentiment_mapping = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

# Function to analyze sentiment of a given text
def analyze_sentiment(text):
    sentiment = sentiment_pipeline(text)[0]
    sentiment_label = sentiment['label']
    sentiment_score = sentiment['score']
    
    # Map the model's internal labels to human-readable ones using the sentiment_mapping dictionary
    sentiment_label_human = sentiment_mapping.get(sentiment_label, "Unknown")  # Default to "Unknown" if label is not found
    
    return sentiment_label_human, sentiment_score
