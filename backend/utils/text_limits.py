def truncate_text(text: str, max_chars: int, suffix: str = "... [truncated]") -> str:
    """Trim text to a character budget, preserving a short suffix marker."""
    if max_chars <= 0 or len(text) <= max_chars:
        return text

    keep = max_chars - len(suffix)
    if keep <= 0:
        return text[:max_chars]

    return text[:keep].rstrip() + suffix
