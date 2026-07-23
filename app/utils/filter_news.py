from app.schemas.schemas import *


def filter_relevant_news(news_collection: NewsArticleCollection, assessment_collection: RelevanceAssessmentCollection) -> NewsArticleCollection:
    articles = []
    article_ids = set()

    for assessment in assessment_collection.assessments:
        if assessment.keep:
            article_ids.add(assessment.article_id)

    for news in news_collection.articles:
        if news.article_id in article_ids:
            articles.append(news)

    return NewsArticleCollection(articles=articles)