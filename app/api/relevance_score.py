from app.llms.llms import *
from app.schemas.schemas import *

from app.prompts.prompts import RELEVANCE_SYSTEM_PROMPT
from app.llms.llms import llm_groq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

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



"""

[
    {
        article_id: "abc",
        relevance_score: 9.5,
        keep: True,
        reason: "Directly discusses a recent AI model."
    },

    {
        article_id: "xyz",
        relevance_score: 2.0,
        keep: False,
        reason: "Sports article with only a passing mention of AI."
    }
]

"""

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