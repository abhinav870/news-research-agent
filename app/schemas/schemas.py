from typing import Literal, List
from pydantic import BaseModel, Field,  HttpUrl
from datetime import datetime


class NewsRequest(BaseModel):
    """
    Structured representation of the user's news request.
    """

    topic: str = Field(..., description = "The topic or domain the user wants news about. Example: AI, Cricket, Politics, Education.")
    duration: Literal["latest", "today", "last_week", "last_month", "over_the_years"] = Field(default = "latest", description = "Time period over which news should be fetched.")
    format: Literal["short", "medium", "long"] = Field(..., description = "Desired length of the final news summary.")

class NewsArticle(BaseModel):
    """
    Represents a single news article/post fetched from a news source.
    This is the output contract of the News Fetch Agent.
    """

    headline: str = Field(..., description="Short descriptive headline of the news article.")
    content: str = Field(..., description="Cleaned news content extracted from the source.")
    source: str = Field(..., description="Platform or publisher from which the news was fetched. Example: Twitter, Reuters, BBC.")
    author: str = Field(..., description="Original author or publisher of the news.")
    url: HttpUrl = Field(..., description="Direct URL pointing to the original news article or post.")
    published_at: datetime = Field(..., description="Date and time when the news was originally published.")
    raw_text: str = Field(..., description="Original unmodified text exactly as fetched from the source.")


class NewsArticleCollection(BaseModel):
    """
    Represents a collection of news articles returned by the
    News Fetch Agent.
    """

    articles: List[NewsArticle] = Field(..., description="List of fetched news articles.")