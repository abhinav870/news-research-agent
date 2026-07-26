from app.graph.state import NewsAgentState

from app.api.fetch_news import fetch_news
from app.api.relevance_score import generate_relevance_scores
from app.api.verification import generate_verification_scores

from app.utils.filter_relevant_news import filter_relevant_news
from app.utils.deduplicate import deduplicate_news
from app.utils.re_ranking import rerank_articles
from app.utils.formatter import format_and_save_news

def fetch_news_node(state: NewsAgentState):

    news_collection = fetch_news(request=state["request"])
    return {"fetched_news": news_collection}

def relevance_node(state: NewsAgentState):

    assessment_collection = generate_relevance_scores(
        request=state["request"],
        news=state["fetched_news"]
    )

    return {"relevance_assessments": assessment_collection}

def filter_node(state: NewsAgentState):

    filtered_news = filter_relevant_news(
        news_collection=state["fetched_news"],
        assessment_collection=state["relevance_assessments"]
    )

    return {"filtered_news": filtered_news}

def deduplicate_node(state: NewsAgentState):

    deduplicated_news = deduplicate_news(
        news_collection=state["filtered_news"],
        assessment_collection=state["relevance_assessments"]
    )

    return {"deduplicated_news": deduplicated_news}

def verify_node(state: NewsAgentState):

    verification_collection = generate_verification_scores(
        news=state["deduplicated_news"]
    )

    return {"verification_assessments": verification_collection}

def rerank_node(state: NewsAgentState):

    reranked_news = rerank_articles(
        request=state["request"],
        news=state["deduplicated_news"],
        relevance_assessments=state["relevance_assessments"],
        verification_assessments=state["verification_assessments"]
    )

    return {"reranked_news": reranked_news}

def formatter_node(state: NewsAgentState):

    file_path = format_and_save_news(
        request=state["request"],
        news_collection=state["reranked_news"]
    )

    return {"markdown_report": str(file_path)}