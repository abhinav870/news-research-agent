from app.llms.llms import *
from app.prompts.prompts import *
from app.llms.llms import llm_groq

from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

def build_reranking_context(
            news: NewsArticleCollection,
            relevance_assessments: RelevanceAssessmentCollection,
            verification_assessments: VerificationAssessmentCollection
) -> str:
    
    """
    1) Build a string representation of the news articles to be used as context for the LLM.
    2) The context will include the article_id, headline, summary, source, relevance_score and credibility_score of each news article.
    3) The context will be used to generate rankings for each news article with respect to the user's news request.
    """

    relevance_lookup = {}
    for assessment in relevance_assessments.assessments:
        relevance_lookup[assessment.article_id] = assessment.relevance_score

    credibility_lookup = {}
    for assessment in verification_assessments.assessments:
        credibility_lookup[assessment.article_id] = assessment.credibility_score

    res = []
    for article in news.articles:

        res.append("Article ID:")
        res.append(article.article_id)

        res.append("Headline:")
        res.append(article.headline)

        res.append("Summary:")
        res.append(article.summary)

        res.append("Source:")
        res.append(article.source)

        res.append("Credibility Score:")
        res.append(str(credibility_lookup.get(article.article_id,"")))

        res.append("Relevance Score:")
        res.append(str(relevance_lookup.get(article.article_id,"")))

        res.append("*"*50)

    return "\n".join(res)


def rerank_articles(request: NewsRequest,
                    news: NewsArticleCollection,
                    relevance_assessments: RelevanceAssessmentCollection,
                    verification_assessments: VerificationAssessmentCollection
                    ) -> NewsArticleCollection:
    """
    1) Generate rank for each news article with respect to the user's news request, relevance_score and credibility_score.
    2) Firstly, get the context of the news articles to be used as input for the LLM (i.e. article_id, headline, summary, source, relevance_score and credibility_score).
    3) Then generate rankings for each news article with respect to the user's news request using the LLM.
    4) Finally, return a new NewsArticleCollection containing the news articles in the order of their rank.

    """

    topic = request.topic
    context = build_reranking_context(news, relevance_assessments, verification_assessments)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', RE_RANKING_SYSTEM_PROMPT),
            ('human',"""

                User Request
                
                Topic:
                {topic}

                Articles:
                {articles}

                """
            )
        ]
    )

    structured_llm_groq = llm_groq.with_structured_output(RankedArticleCollection)

    chain = prompt | structured_llm_groq
    response = chain.invoke({
        "topic": topic,
        "articles": context
    }) # This is Step-1


    """
    ALGORITHM USED:

    1) Get the ranked article_ids from LLM (random ranks)
    2) Store the article_id and its rank in a dictionary and sort the dictionary to get the articles in ascending order of their rank.
    3) Store the article_id and its corresponding NewsArticle object in a dictionary for easy access later.
    4) Prepare a new list of NewsArticle objects in the order of their rank to return as a new NewsArticleCollection.
    
    """

    # Step-2
    article_ranking = {} # Storing article id and its rank in a dictionary for sorting later
    for ranked_article in response.rankings:
        article_ranking[ranked_article.article_id] = ranked_article.rank

    article_ranking = dict(sorted(article_ranking.items(), key=lambda x: x[1])) # Sort this dictionary to get the artiles in asc order of their rank

    # Step-3
    articles_info = {} # Store the article_id and its corresponding NewsArticle object in a dictionary for easy access later
    for article in news.articles:
        articles_info[article.article_id] = article

    #  Step-4 
    re_ranked_articles = [] # Prepare a new list of NewsArticle objects in the order of their rank to return as a new NewsArticleCollection
    for article_id, rank in article_ranking.items():
        re_ranked_articles.append(
            NewsArticle(
                article_id=article_id,
                headline=articles_info[article_id].headline,
                summary=articles_info[article_id].summary,
                source=articles_info[article_id].source,
                author=articles_info[article_id].author,
                url=articles_info[article_id].url,
                published_at=articles_info[article_id].published_at,
                raw_text=articles_info[article_id].raw_text
            )
        )

    return NewsArticleCollection(articles=re_ranked_articles)