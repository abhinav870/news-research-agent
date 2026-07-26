from langgraph.graph import StateGraph, START, END
from app.graph.state import NewsAgentState
from app.graph.nodes import fetch_news_node, relevance_node, filter_node, deduplicate_node, verify_node, rerank_node, formatter_node

builder = StateGraph(NewsAgentState)

# -----------------------
# Add Nodes
# -----------------------

builder.add_node("fetch_news", fetch_news_node)
builder.add_node("generate_relevance_scores", relevance_node)
builder.add_node("filter_news", filter_node)
builder.add_node("deduplicate_news", deduplicate_node)
builder.add_node("generate_verification_scores", verify_node)
builder.add_node("rerank_articles", rerank_node)
builder.add_node("format_news", formatter_node)

# -----------------------
# Add Edges
# -----------------------

builder.add_edge(START, "fetch_news")
builder.add_edge("fetch_news", "generate_relevance_scores")
builder.add_edge("generate_relevance_scores", "filter_news")
builder.add_edge("filter_news", "deduplicate_news")
builder.add_edge("deduplicate_news", "generate_verification_scores")
builder.add_edge("generate_verification_scores", "rerank_articles")
builder.add_edge("rerank_articles", "format_news")
builder.add_edge("format_news", END)


# -----------------------
# Compile Graph
# -----------------------

graph = builder.compile()