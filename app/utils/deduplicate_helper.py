from app.schemas.schemas import NewsArticle
from rapidfuzz import fuzz
from datetime import timedelta


def headline_similarity(article1: NewsArticle, article2: NewsArticle) -> float:
    """
    Returns headline similarity between 0 and 1.
    """
    return fuzz.token_set_ratio(article1.headline, article2.headline) / 100.0


def time_similarity(article1: NewsArticle, article2: NewsArticle) -> float:
    """
    Returns similarity based on publication time.
    """

    hours = abs((article1.published_at - article2.published_at).total_seconds()) / 3600

    if hours <= 6:
        return 1.0
    
    elif hours <= 24:
        return 0.8

    elif hours <= 72:
        return 0.5

    else:
        return 0.2