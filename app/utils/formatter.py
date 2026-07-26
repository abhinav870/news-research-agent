from pathlib import Path
from datetime import datetime
from datetime import datetime
import re

from app.schemas.schemas import NewsRequest, NewsArticleCollection


def format_news(request: NewsRequest, news_collection: NewsArticleCollection ) -> str:
    """
    Formats the ranked news into Markdown.
    """

    markdown = []
    markdown.append("# 📰 AI News Research Report\n")

    markdown.append("## Search Details\n")
    markdown.append(f"- **Topic:** {request.topic}")
    markdown.append(f"- **Duration:** {request.duration}")
    markdown.append(f"- **Generated On:** {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    markdown.append(f"- **Articles Returned:** {len(news_collection.articles)}\n")

    markdown.append("---\n")

    if len(news_collection.articles) == 0:
        markdown.append("No relevant news articles found.")
        return "\n".join(markdown)

    for idx, article in enumerate(news_collection.articles, start=1):

        markdown.append(f"## {idx}. {article.headline}\n")
        markdown.append(f"**Source:** {article.source}")

        if article.published_at:
            markdown.append(f"  |  **Published:** {article.published_at}")

        markdown.append("")

        markdown.append("### Summary")
        markdown.append(article.summary)
        markdown.append("")

        if article.url:
            markdown.append(f"**Read More:** {article.url}")
            markdown.append("")

        markdown.append("---\n")

    return "\n".join(markdown)


def save_markdown(markdown_content: str, topic: str, output_dir: str = "outputs" ) -> Path:
    """
    Saves markdown content to disk.

    File name format:
    <topic_name>_<YYYYMMDD_HHMMSS>.md
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Sanitize topic
    topic = topic.strip()
    topic = re.sub(r"\s+", "_", topic)
    topic = re.sub(r"[^A-Za-z0-9_-]", "", topic)

    # Current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{topic}_{timestamp}.md"
    file_path = output_path / file_name
    file_path.write_text(markdown_content, encoding="utf-8")

    return file_path


def format_and_save_news(request: NewsRequest, news_collection: NewsArticleCollection, output_dir: str = "outputs") -> Path:
    """
    Formats the news and saves it as a Markdown file.
    """

    markdown = format_news(request, news_collection)

    return save_markdown(
        markdown_content=markdown,
        topic=request.topic,
        output_dir=output_dir
    )