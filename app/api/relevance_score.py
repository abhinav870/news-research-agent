from app.llms.llms import *
from app.schemas.schemas import *

from app.prompts.prompts import RELEVANCE_SYSTEM_PROMPT
from app.llms.llms import llm_groq
from app.api.fetch_news import fetch_news

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

def build_article_context(news: NewsArticleCollection) -> str:

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

        res.append("*"*50)

    return "\n".join(res)


def filter_news(request: NewsRequest, news: NewsArticleCollection) -> RelevanceAssessmentCollection:

    context = build_article_context(news)
    topic = request.topic
    duration = request.duration

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', RELEVANCE_SYSTEM_PROMPT),
            ('human',"""

                User Request
                
                Topic:
                {topic}

                Duration:
                {duration}

                Articles:
                {articles}

                """
            )
        ]
    )

    structured_llm_groq = llm_groq.with_structured_output(RelevanceAssessmentCollection)

    chain = prompt | structured_llm_groq
    response = chain.invoke({
        "topic": topic,
        "duration": duration,
        "articles": context,
    })

    return response

if __name__== "__main__":

    request = NewsRequest(
        topic="Artificial Intelligence",
        duration="latest",
        format="short"
    )

    news = fetch_news(request)

    pprint(type(news))
    pprint(news)

    print("*"*100)

    assessment = filter_news(request, news)
    pprint(assessment.model_dump_json(indent=4))