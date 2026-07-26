from typing_extensions import TypedDict
from app.schemas.schemas import *

class NewsAgentState(TypedDict):
    request: NewsRequest
    fetched_news: NewsArticleCollection

    relevance_assessments: RelevanceAssessmentCollection

    filtered_news: NewsArticleCollection
    deduplicated_news: NewsArticleCollection

    verification_assessments: VerificationAssessmentCollection

    verified_news: NewsArticleCollection
    reranked_news: NewsArticleCollection

    markdown_report: str