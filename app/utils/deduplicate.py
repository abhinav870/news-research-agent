from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

from app.schemas.schemas import *
from app.utils.deduplicate_helper import headline_similarity, time_similarity

# Load once
# SIMILARITY_THRESHOLD = 0.83
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
HIGH_EMBEDDING_THRESHOLD = 0.90

MEDIUM_EMBEDDING_THRESHOLD = 0.82
MEDIUM_HEADLINE_THRESHOLD = 0.60

LOW_EMBEDDING_THRESHOLD = 0.78
LOW_HEADLINE_THRESHOLD = 0.70
LOW_TIME_THRESHOLD = 0.80

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

            Source:
            {article.source}

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

            # similarity = similarity_matrix[i][j]
            # if similarity >= SIMILARITY_THRESHOLD:
            #     graph.add_edge(news_collection.articles[i].article_id, news_collection.articles[j].article_id)

            article1 = news_collection.articles[i]
            article2 = news_collection.articles[j]
            
            embedding_score = similarity_matrix[i][j]
            headline_score = headline_similarity(news_collection.articles[i], news_collection.articles[j])
            time_score = time_similarity(news_collection.articles[i], news_collection.articles[j])

            is_duplicate = False
            matched_rule = ""

            # Rule 1: Extremely high semantic similarity
            if embedding_score >= HIGH_EMBEDDING_THRESHOLD: 
                is_duplicate = True
                matched_rule = "High Semantic Similarity"

            # Rule 2: Moderate semantic similarity + similar headlines
            elif embedding_score >= MEDIUM_EMBEDDING_THRESHOLD and headline_score >= MEDIUM_HEADLINE_THRESHOLD:
                is_duplicate = True
                matched_rule = "Semantic + Headline Similarity"

             # Rule 3: Slightly lower semantic similarity, compensated by very similar headlines and publication time
            elif LOW_EMBEDDING_THRESHOLD <= embedding_score < MEDIUM_EMBEDDING_THRESHOLD and headline_score >= LOW_HEADLINE_THRESHOLD and time_score >= LOW_TIME_THRESHOLD:
                is_duplicate = True
                matched_rule = "Semantic + Headline + Time Similarity"

            if is_duplicate:
                graph.add_edge(article1.article_id, article2.article_id)

                print("=" * 100)

                print(article1.headline)
                print(article2.headline)

                print(f"Embedding : {embedding_score:.2f}")
                print(f"Headline  : {headline_score:.2f}")
                print(f"Time      : {time_score:.2f}")
                print(f"Matched   : {matched_rule}")

                print("✅ Duplicate\n")

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
