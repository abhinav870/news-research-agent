# fetch_news.py
import os
import requests

from dotenv import load_dotenv
from app.schemas.schemas import NewsRequest
from pprint import pprint

load_dotenv()

# NewsData.io endpoint
BASE_URL = "https://newsdata.io/api/1/latest"


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
    return raw_json

if __name__ == "__main__":

    request = NewsRequest(
        # topic="Artificial Intelligence",
        # topic = "International Men's Cricket",
        topic = "Indian Politics",
        duration="latest",
        format="short"
    )

    response = fetch_news(request)
    pprint(response)