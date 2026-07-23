from app.schemas.schemas import *
from app.prompts.prompts import DUPLICATE_SYSTEM_PROMPT
from app.llms.llms import llm_groq

from dotenv import load_dotenv
from pprint import pprint
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def deduplicate_news(news_collection: NewsArticleCollection) -> NewsArticleCollection:
    """
    1) Deduplicate news articles based on their headlines and summary.
    2) Fetch the article ids of the duplicate articles and group them together.
    3) For each group of duplicate articles, select the article with the highest relevance score.
    4) Return a new NewsArticleCollection containing only the deduplicated articles.
    """

    articles = []
    for article in news_collection.articles:

        articles.append(
            {
                "article_id": article.article_id,
                "headline": article.headline,
                "summary": article.summary,
                "relevance_score": article.relevance_score          
            }
        )

    llm_structured_output = llm_groq.with_structured_output(DuplicateGroups)
    prompt = ChatPromptTemplate.from_messages(
        [   
            ('system',DUPLICATE_SYSTEM_PROMPT),
            (
                'human',
                """ 
                Articles:
                {articles}
                """
            )
        ]
    )    

    chain = prompt | llm_structured_output
    response = chain.invoke({'articles': articles})

    '''
    1) Dedupe the news articles based on their headlines and summary.
    2) Fetch the article ids of the duplicate articles and group them together.
    3) For each group of duplicate articles, select the article with the highest relevance score.
    '''

    deduplicated_articles = []
    for group in response.groups:

        group_articles = []
        curr_grp_ids = set(group.article_ids) # Get the grp article ids having duplicate headline and summary

        for article in news_collection.articles: # Iterate through all articles and find the curr duplicated articles
            if article.article_id in curr_grp_ids:
                group_articles.append(article)

        best_article = max(group_articles, key = lambda x: x.relevance_score) # Fetch the best article based on the highest relevance score
        deduplicated_articles.append(best_article)

    return NewsArticleCollection(articles=deduplicated_articles)