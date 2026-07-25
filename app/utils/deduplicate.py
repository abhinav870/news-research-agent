from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

from app.schemas.schemas import *


# Load once
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = 0.88


def deduplicate_news(news_collection: NewsArticleCollection, assessment_collection: RelevanceAssessmentCollection) -> NewsArticleCollection:
    """
    1. Convert every news article into an embedding (vector)
    2. Compute pairwise cosine similarity between all article embeddings
    3. Build a graph where each article is a node, and an edge exists between two articles if their similarity exceeds a threshold.
    4. Identify connected components in the graph, where each component represents a group of duplicate articles.
    5. For each group of duplicates, select the article with the highest relevance score to retain.
    6. Return a new NewsArticleCollection containing only the retained articles.
    """

    if len(news_collection.articles) <= 1:
        return news_collection

    # Lookup relevance score
    score_lookup = {}
    for assessment in assessment_collection.assessments:
        score_lookup[assessment.article_id] = assessment.relevance_score

    # Build embedding text
    texts = []
    for article in news_collection.articles:

        texts.append(
        f"""
            Headline:
            {article.headline}

            Summary:
            {article.summary}
        """
    )

    embeddings = embedding_model.encode(texts, normalize_embeddings=True)
    similarity_matrix = cosine_similarity(embeddings)
    
    # Build graph
    graph = nx.Graph()

    for article in news_collection.articles:
        graph.add_node(article.article_id)

    for i in range(len(news_collection.articles)):
        for j in range(i + 1, len(news_collection.articles)):

            similarity = similarity_matrix[i][j]

            if similarity >= SIMILARITY_THRESHOLD:
                graph.add_edge(news_collection.articles[i].article_id, news_collection.articles[j].article_id)

    # Connected Components
    deduplicated_articles = []
    article_lookup = {}

    for article in news_collection.articles:
        article_lookup[article.article_id] = article

    print("\nDuplicate Groups\n")

    for component in nx.connected_components(graph):
        print(component)

        group_articles = []
        for article_id in component:
            group_articles.append(article_lookup[article_id])


        best_article = max(group_articles, key=lambda article: score_lookup.get(article.article_id, 0))
        deduplicated_articles.append(best_article)

    return NewsArticleCollection(articles=deduplicated_articles)
