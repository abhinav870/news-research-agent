from app.schemas.schemas import *

from app.api.fetch_news import fetch_news
from app.api.relevance_score import generate_relevance_scores
from app.api.verification import generate_verification_scores

from app.utils.deduplicate import deduplicate_news
from app.utils.filter_news import filter_relevant_news
from app.utils.filter_verified_news import filter_verified_news

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
        topic="Indian Politics",
        duration="latest",
        format="short",
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
    # Assertions
    ####################################################################

    assert len(filtered_news.articles) <= len(news_collection.articles)

    assert len(deduplicated_news.articles) <= len(filtered_news.articles)

    assert len(verified_news.articles) <= len(deduplicated_news.articles)

    article_ids = [
        article.article_id
        for article in verified_news.articles
    ]

    assert len(article_ids) == len(set(article_ids))

    print("\n" + "=" * 80)
    print("PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()