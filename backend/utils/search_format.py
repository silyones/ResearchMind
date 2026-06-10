from typing import List

from backend.config import settings
from backend.utils.text_limits import truncate_text


def format_search_results(results: List[dict]) -> str:
    """Format Tavily results as compact text for synthesis."""
    if not results:
        return "No search results found."

    lines = []
    for index, result in enumerate(results, start=1):
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        content = result.get("content", "")
        published = result.get("published_date") or "Unknown date"
        lines.append(
            f"[Source {index}]\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Date: {published}\n"
            f"Content: {content}"
        )

    return truncate_text("\n\n".join(lines), settings.max_context_chars)
