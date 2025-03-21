import feedparser
import concurrent.futures
from rapidfuzz import fuzz
import requests
from bs4 import BeautifulSoup

# List of news sources with RSS Feeds
NEWS_SOURCES = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best",
    "The Guardian": "https://www.theguardian.com/uk/rss",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Wired": "https://www.wired.com/feed/rss",
    "The Independent": "https://www.independent.co.uk/news/uk/rss",
    "NY Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "Financial Times": "https://www.ft.com/rss/home",
    "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index/",
    "ABC News": "https://abcnews.go.com/abcnews/topstories",
    "CBS News": "https://www.cbsnews.com/latest/rss/main",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
}

# Function to fetch RSS headlines matching a company
def get_matching_headlines(company_name):
    matching_headlines = []

    def process_feed(feed_url):
        try:
            feed = feedparser.parse(feed_url)
            for article in feed.entries:
                title = article.title
                link = article.link
                description = article.description if hasattr(article, "description") else ""

                # Use fuzzy matching
                if (
                    fuzz.token_set_ratio(company_name.lower(), title.lower()) > 85 or
                    fuzz.token_set_ratio(company_name.lower(), description.lower()) > 85
                ):
                    return title, link
        except Exception as e:
            print(f"⚠️ RSS Feed Error: {e}")
        return None

    # Use threading for faster RSS fetch
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_feed, url) for url in NEWS_SOURCES.values()]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                matching_headlines.append(result)

    return matching_headlines

# Function to scrape non-JS articles
def scrape_article(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        divs = soup.find_all("div")
        article_text = " ".join([p.get_text() for p in paragraphs]) if paragraphs else " ".join([d.get_text() for d in divs])
        return article_text.strip() if article_text else None

    except requests.RequestException as e:
        print(f"⚠️ Request Error: {e}")
        return None
