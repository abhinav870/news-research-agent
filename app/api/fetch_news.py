# fetch_news.py
import os
import requests

from dotenv import load_dotenv
from app.schemas.schemas import NewsRequest, NewsArticle, NewsArticleCollection
from pprint import pprint

load_dotenv()

# NewsData.io endpoint
BASE_URL = "https://newsdata.io/api/1/latest"

def parse_news(raw_json: dict) -> NewsArticleCollection:
    articles = []

    for article in raw_json.get("results", []):

        title = article.get("title")
        description = article.get("description")
        link = article.get("link")
        source = article.get("source_name")
        pub_date = article.get("pubDate")
        article_id = article.get("article_id")

        if not all([article_id, title, description, link, source, pub_date]):
            continue

        articles.append(
            NewsArticle(
                article_id=article_id,
                headline=title,
                summary=description,
                source=source,
                author=article.get("creator"),
                url=link,
                published_at=pub_date,
                raw_text=f"{title}\n\n{description}",
            )
        )

    return NewsArticleCollection(articles=articles)

def fetch_news(request: NewsRequest):

    # -----------------------------------------
    # Step 1 : Build API Request
    # -----------------------------------------

    topic = request.topic
    duration = request.duration
    api_key = os.getenv("NEWSDATA_API_KEY")

    if not api_key:
        raise ValueError("NEWSDATA_API_KEY not found in environment variables.")

    params = {
        "apikey": api_key,
        "q": topic,
        "language": "en"
    }

    # Optional filters
    if duration != "latest":
        params["timeframe"] = duration

    # -----------------------------------------
    # Step 2 : Hit API
    # -----------------------------------------

    response = requests.get(BASE_URL, params=params, timeout=30)
    raw_json = response.json()

    return parse_news(raw_json)