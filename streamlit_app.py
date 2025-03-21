import streamlit as st
import json
from main import process_company_news_with_audio

st.title("Company News Summary and Audio")

# Text input for the company name
company_name = st.text_input("Enter the company name:")

if company_name:
    st.write(f"Processing news for {company_name}...")

    # Call the function to process the news and generate audio
    summary_json = process_company_news_with_audio(company_name)

    # Display the summary and sentiment analysis
    if summary_json:
        st.subheader("News Summary")
        for article in summary_json["Articles"]:
            st.write(f"**Title:** {article['Title']}")
            st.write(f"**Summary:** {article['Summary']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
            
            # Use .get() to avoid KeyError and display a default message if 'Summary Sentiment' is missing
            st.write(f"**Summary Sentiment:** {article.get('Summary Sentiment', 'Not available')}")
        
        # Play the audio
        audio_file = summary_json.get("Audio", None)
        if audio_file:
            st.audio(audio_file)
    else:
        st.write(f"No news found for {company_name}.")
