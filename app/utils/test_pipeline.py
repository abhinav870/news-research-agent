import nt

from app.schemas.schemas import *

from app.api.fetch_news import fetch_news
from app.api.relevance_score import generate_relevance_scores
from app.api.verification import generate_verification_scores

from app.utils.deduplicate import deduplicate_news
from app.utils.filter_relevant_news import filter_relevant_news
from app.utils.filter_relevant_verified_news import filter_verified_news
from app.utils.re_ranking import rerank_articles
from app.utils.formatter import format_and_save_news

from dotenv import load_dotenv
load_dotenv()


def print_stage(
    stage_name: str,
    news_collection: NewsArticleCollection,
    relevance_assessments: RelevanceAssessmentCollection | None = None,
    verification_assessments: VerificationAssessmentCollection | None = None,
) -> None:
    """
    Pretty print all articles present at a pipeline stage.
    """

    relevance_lookup = {}
    verification_lookup = {}

    if relevance_assessments is not None:
        relevance_lookup = {
            assessment.article_id: assessment.relevance_score
            for assessment in relevance_assessments.assessments
        }

    if verification_assessments is not None:
        verification_lookup = {
            assessment.article_id: assessment.credibility_score
            for assessment in verification_assessments.assessments
        }

    print("\n" + "=" * 80)
    print(stage_name.upper())
    print("=" * 80)

    print(f"Total Articles : {len(news_collection.articles)}\n")

    for article in news_collection.articles:

        print(f"Article ID        : {article.article_id}")
        print(f"Headline          : {article.headline}")
        print(f"Summary           : {article.summary}")

        if article.article_id in relevance_lookup:
            print(
                f"Relevance Score   : {relevance_lookup[article.article_id]:.2f}"
            )

        if article.article_id in verification_lookup:
            print(
                f"Credibility Score : {verification_lookup[article.article_id]:.2f}"
            )

        print(f"Source            : {article.source}")
        print("-" * 80)


def main():

    ####################################################################
    # User Request
    ####################################################################

    # request = NewsRequest(
    #     topic="Artificial Intelligence",
    #     duration="latest",
    #     format="short",
    # )

    request = NewsRequest(
        topic="International Men's Cricket",
        duration="latest",
        format="long"
    )

    ####################################################################
    # Step 1 : Fetch News
    ####################################################################

    news_collection = fetch_news(request)

    print_stage(
        "Step 1 : Fetched News",
        news_collection,
    )

    ####################################################################
    # Step 2 : Generate Relevance Scores
    ####################################################################

    relevance_assessments = generate_relevance_scores(
        request,
        news_collection,
    )

    ####################################################################
    # Step 3 : Filter Relevant News
    ####################################################################

    filtered_news = filter_relevant_news(
        news_collection,
        relevance_assessments,
    )

    print_stage(
        "Step 2 : Relevant News",
        filtered_news,
        relevance_assessments=relevance_assessments,
    )

    ####################################################################
    # Step 4 : Deduplicate News
    ####################################################################

    deduplicated_news = deduplicate_news(
        filtered_news,
        relevance_assessments,
    )

    print_stage(
        "Step 3 : Deduplicated News",
        deduplicated_news,
        relevance_assessments=relevance_assessments,
    )

    ####################################################################
    # Step 5 : Generate Verification Scores
    ####################################################################

    verification_assessments = generate_verification_scores(
        deduplicated_news,
    )

    ####################################################################
    # Step 6 : Filter Verified News
    ####################################################################

    verified_news = filter_verified_news(
        deduplicated_news,
        verification_assessments,
    )

    print_stage(
        "Step 4 : Verified News",
        verified_news,
        relevance_assessments=relevance_assessments,
        verification_assessments=verification_assessments,
    )

    ####################################################################
    # Debug : Order Before Re-ranking
    ####################################################################

    print("\n" + "=" * 80)
    print("ORDER BEFORE RE-RANKING")
    print("=" * 80)

    for idx, article in enumerate(verified_news.articles, start=1):
        print(f"{idx}. {article.headline}")

    print()

    ####################################################################
    # Step 7 : Re-rank Articles
    ####################################################################

    reranked_news = rerank_articles(
        request,
        verified_news,
        relevance_assessments,
        verification_assessments,
    )

    print_stage(
        "Step 5 : Re-ranked News",
        reranked_news,
        relevance_assessments=relevance_assessments,
        verification_assessments=verification_assessments,
    )

    ####################################################################
    # Debug : Order After Re-ranking
    ####################################################################

    print("\n" + "=" * 80)
    print("ORDER AFTER RE-RANKING")
    print("=" * 80)

    for idx, article in enumerate(reranked_news.articles, start=1):
        print(f"{idx}. {article.headline}")

    print()

    output_path = format_and_save_news(
        request=request,
        news_collection=reranked_news,
    )

    print(f"\nMarkdown report saved to: {output_path}")

   ####################################################################
    # Assertions
    ####################################################################

    # Filtering should never increase the number of articles
    assert len(filtered_news.articles) <= len(news_collection.articles)

    # Deduplication should never increase the number of articles
    assert len(deduplicated_news.articles) <= len(filtered_news.articles)

    # Verification filtering should never increase the number of articles
    assert len(verified_news.articles) <= len(deduplicated_news.articles)

    # Re-ranking should preserve the number of articles
    assert len(reranked_news.articles) == len(verified_news.articles)

    # No duplicate article IDs after verification
    verified_article_ids = [
        article.article_id
        for article in verified_news.articles
    ]
    assert len(verified_article_ids) == len(set(verified_article_ids))

    # Re-ranking should not lose or introduce any articles
    assert {
        article.article_id
        for article in verified_news.articles
    } == {
        article.article_id
        for article in reranked_news.articles
    }

    print("\n" + "=" * 80)
    print("PIPELINE EXECUTED SUCCESSFULLY (INCLUDING RE-RANKING)")
    print("=" * 80)


if __name__ == "__main__":
    main()