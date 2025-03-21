import json
from news_fetcher import get_matching_headlines
from summarizer import summarize_text
from sentiment_analyzer import analyze_sentiment
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from gtts import gTTS
from news_fetcher import scrape_article
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Import stopwords from nltk
from nltk.corpus import stopwords

# Function to extract key terms from a headline using TF-IDF
def extract_key_terms_from_headline(headline, top_n=5):
    stop_words = stopwords.words('english')
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=10)
    tfidf_matrix = tfidf_vectorizer.fit_transform([headline])  # Notice the list to handle single input
    feature_names = tfidf_vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1  # Convert to 1D array
    term_score_pairs = [(feature_names[i], scores[i]) for i in range(len(feature_names))]
    sorted_term_score_pairs = sorted(term_score_pairs, key=lambda x: x[1], reverse=True)
    key_terms = [term for term, score in sorted_term_score_pairs[:top_n]]
    return key_terms

# Refined Coverage Differences: More in-depth comparison of topics
def get_coverage_differences(article1_summary, article2_summary):
    # Instead of using the first part, we will use the entire summary and focus on the issues
    comparison = {
        "Comparison": "Article 1 discusses {0}, while Article 2 covers {1}.".format(
            article1_summary[:100], article2_summary[:100]),
        "Impact": "The first article focuses on {0}, while the second article raises concerns about {1}.".format(
            article1_summary[:50], article2_summary[:50])
    }
    return comparison

# Function to extract common and unique topics from articles
def get_topic_overlap(article1_text, article2_text):
    # Extract key terms from both articles
    terms1 = extract_key_terms_from_headline(article1_text)
    terms2 = extract_key_terms_from_headline(article2_text)
    
    common_topics = list(set(terms1) & set(terms2))
    unique_topics_1 = list(set(terms1) - set(terms2))
    unique_topics_2 = list(set(terms2) - set(terms1))

    return {
        "Common Topics": common_topics,
        "Unique Topics in Article 1": unique_topics_1,
        "Unique Topics in Article 2": unique_topics_2
    }

# Main function to analyze news for a company
def process_company_news(company_name):
    # Sentiment counters for headlines and summaries
    headline_sentiment_count = {"Positive": 0, "Neutral": 0, "Negative": 0}
    summary_sentiment_count = {"Positive": 0, "Neutral": 0, "Negative": 0}
    
    headlines = get_matching_headlines(company_name)

    if not headlines:
        print(f"❌ No news headlines found for '{company_name}'.")
        return None  # Return None if no headlines are found

    articles = []
    article_summaries = []
    for title, url in headlines:
        article_data = {}
        article_data["Title"] = title
        article_data["Summary"] = ""

        # Extract key terms from the headline
        key_terms = extract_key_terms_from_headline(title, top_n=5)
        article_data["Topics"] = key_terms

        # Sentiment on headline
        headline_sentiment, headline_score = analyze_sentiment(title)
        article_data["Sentiment"] = headline_sentiment

        # Update sentiment counters for headlines
        if headline_sentiment == "Positive":
            headline_sentiment_count["Positive"] += 1
        elif headline_sentiment == "Neutral":
            headline_sentiment_count["Neutral"] += 1
        elif headline_sentiment == "Negative":
            headline_sentiment_count["Negative"] += 1

        # Scrape and summarize article
        article_text = scrape_article(url)
        if article_text:
            summary = summarize_text(article_text)
            article_summaries.append(summary)
            article_data["Summary"] = summary

            # Sentiment on summary
            summary_sentiment, summary_score = analyze_sentiment(summary)
            article_data["Summary Sentiment"] = summary_sentiment

            # Update sentiment counters for summaries
            if summary_sentiment == "Positive":
                summary_sentiment_count["Positive"] += 1
            elif summary_sentiment == "Neutral":
                summary_sentiment_count["Neutral"] += 1
            elif summary_sentiment == "Negative":
                summary_sentiment_count["Negative"] += 1
        else:
            print("❌ Failed to extract full article.")

        articles.append(article_data)
    
    # Prepare JSON output
    output = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": headline_sentiment_count,
            "Coverage Differences": [],  # Add this based on your logic
            "Topic Overlap": {}  # Add this based on your logic
        },
        "Final Sentiment Analysis": "Positive coverage overall." if summary_sentiment_count["Positive"] > summary_sentiment_count["Negative"] else "Mixed or Negative coverage overall."
    }

    return output  # Return the JSON result

# Function to extract summaries and translate them
def generate_hindi_audio_from_summary(json_summary, audio_path="D:\\NewsSummarizer\\Audio\\company_news_summary_hindi.wav"):
    # Check if json_summary is None or if Articles are missing
    if json_summary is None:
        print("Error: json_summary is None.")
        return
    if "Articles" not in json_summary:
        print("Error: 'Articles' not found in json_summary.")
        return
    
    # Extract the summaries from the JSON
    summaries = []
    for article in json_summary["Articles"]:
        if article is None:
            print("Warning: Found a None article. Skipping.")
            continue  # Skip if the article is None
        
        # Check if the article contains a "Summary" field
        if "Summary" not in article:
            print(f"Warning: 'Summary' key missing in article: {article}")
            continue  # Skip if no summary exists
        
        summary = article.get("Summary", "")
        if summary:  # Only add non-empty summaries
            summaries.append(summary)
        else:
            print(f"Warning: Empty summary in article: {article}")

    if not summaries:
        print("Error: No valid summaries available.")
        return
    
    # Combine all summaries into one text block to be read
    summary_text = " ".join(summaries)

    # Load Facebook's mBART model (better multilingual translation)
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)

    # Set source (English) and target (Hindi) languages
    tokenizer.src_lang = "en_XX"
    target_lang = "hi_IN"

    # Tokenize input text
    inputs = tokenizer([summary_text], return_tensors="pt", padding=True, truncation=True)

    # Generate translations
    generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    # Print translated text (optional)
    print("Translated Text in Hindi:", translated_text)

    # Convert translations to speech using Google TTS
    speech = gTTS(text=translated_text, lang="hi", slow=False)
    
    # Save the speech to the specified audio path
    speech.save(audio_path)

    print(f"Audio saved at: {audio_path}")

# Integrate this with your existing process_company_news function
def process_company_news_with_audio(company_name):
    # Generate the summary as usual
    summary_json = process_company_news(company_name)

    if summary_json:
        # Specify the path where the audio file will be saved
        audio_path = "D:\\NewsSummarizer\\Audio\\company_news_summary_hindi.wav"
        
        # Generate Hindi Audio from JSON summary
        generate_hindi_audio_from_summary(summary_json, audio_path)

        # Include the path to the audio file in the JSON output
        summary_json["Audio"] = audio_path
        
        # Print or save the JSON result with the audio file path
        print(json.dumps(summary_json, indent=4))
    
    return summary_json  # Return the JSON result with the audio path

