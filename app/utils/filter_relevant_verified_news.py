from app.schemas.schemas import *

def filter_verified_news(news_collection: NewsArticleCollection, assessment_collection: VerificationAssessmentCollection) -> NewsArticleCollection:
    '''
    1) Filter the news articles based on the assessments generated.
    2) VerificationAssessmentCollection contains the article_ids and verification_status of the news articles.
    3) Fetch the article_ids of the news articles that have verification_status=True and return a new NewsArticleCollection containing only those articles.
    '''

    article_ids = set()
    for assessment in assessment_collection.assessments:
        if assessment.keep and assessment.credibility_score >=6.0:
        # if assessment.keep:
            article_ids.add(assessment.article_id)

    articles = []
    for news in news_collection.articles:
        if news.article_id in article_ids:
            articles.append(news)

    return NewsArticleCollection(articles=articles)