News Summarization and Text-to-Speech Application
Overview
This project is a web-based News Summarization and Text-to-Speech (TTS) Application that extracts, summarizes, and analyzes sentiment from news articles related to a given company. It converts the summary into Hindi speech using a text-to-speech model.

The application is built using:

-> distilBERT (fine-tuned on the tweet_eval dataset) for sentiment analysis
-> T5-small for text summarization
-> facebook/mbart-large-50-many-to-many-mmt for English-to-Hindi translation
-> Postman for API communication between the frontend and backend
While Colab's GPU was used for fine-tuning the sentiment model, all remaining processing runs on the local system CPU.

Features
✔️ Sentiment Analysis categorizing news into Positive, Negative, or Neutral
✔️ Comparative Analysis to highlight sentiment variations across different articles
✔️ Converts summarized text into Hindi speech using an open-source TTS model
✔️ User-friendly Streamlit frontend for easy interaction
✔️ API-based backend communication using Flask

Project Structure
bash
Copy
Edit
NewsSummarizer/
│── myenv/                     # Virtual environment
│── requirements.txt           # Dependencies
│── README.md                  # Documentation
│── app.py                     # Flask backend
│── main.py                    # Core processing logic
│── news_fetcher.py            # Fetch RSS headlines and scrape non-JS articles
│── sentiment_analyzer.py      # Sentiment analysis using distilBERT
│── streamlit_app.py           # Frontend UI (Streamlit)
│── summarizer.py              # Text summarization using T5-small
Setup Instructions
1. Create and Activate Virtual Environment
bash
python -m venv myenv
myenv/Scripts/activate  # On Windows
source myenv/bin/activate  # On macOS/Linux
2. Install Dependencies
bash
pip install -r requirements.txt
3. Run the Backend (Flask)
bash
python app.py
4. Run the Frontend (Streamlit)
bash
python -m streamlit run streamlit_app.py
Usage
Enter the company name in the Streamlit UI.
The system fetches and summarizes relevant news articles.
Sentiment analysis is performed for each article.
A comparative analysis is generated to highlight sentiment trends.
The summarized content is converted to Hindi speech, playable in the UI.
API Endpoints
API Endpoints
-------------------------------------------------------------------------------------------------
| Endpoint         | Method | Description                                                       |
|------------------|--------|-------------------------------------------------------------------|
| /process_news    | POST   | Fetches news, summarizes, analyzes sentiment, and returns results |
| /generate_audio  | POST   | Converts summary text to Hindi speech                             |
-------------------------------------------------------------------------------------------------
APIs can be tested using Postman.
