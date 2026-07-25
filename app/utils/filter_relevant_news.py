from app.schemas.schemas import *

def filter_relevant_news(news_collection: NewsArticleCollection, assessment_collection: RelevanceAssessmentCollection) -> NewsArticleCollection:
    '''
    1) Filter the news articles based on the assessments generated.
    2) RelevanceAssessmentCollection contains the article_ids, relevance_score and keep (True or False) of the news articles that are relevant to the user's request.
    3) Fetch the article_ids of the news articles that have keep=True and return a new NewsArticleCollection containing only those articles.
    '''

    article_ids = set()
    for assessment in assessment_collection.assessments:
        if assessment.keep:
            article_ids.add(assessment.article_id)

    articles = []
    for news in news_collection.articles:
        if news.article_id in article_ids:
            articles.append(news)

    return NewsArticleCollection(articles=articles)