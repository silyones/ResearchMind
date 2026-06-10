import re
from typing import Any


def _safe_filename(topic: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", topic or "research").strip().lower()
    slug = re.sub(r"[\s_-]+", "_", slug)
    return (slug[:60] or "research_report") + ".md"


def build_markdown_report(research: dict[str, Any]) -> str:
    lines = [f"# {research.get('topic', 'Research Report')}", ""]

    overview = research.get("overview", "")
    if overview:
        lines.extend(["## Executive Summary", "", overview, ""])

    report = research.get("report", "")
    if report:
        lines.extend(["## Research Report", "", report, ""])

    findings = research.get("key_findings") or []
    if findings:
        lines.extend(["## Key Findings", ""])
        for index, finding in enumerate(findings, start=1):
            lines.append(f"{index}. {finding.get('finding', '')}")
        lines.append("")

    controversies = research.get("controversies") or []
    if controversies:
        lines.extend(["## Controversies & Debates", ""])
        for item in controversies:
            lines.append(f"- {item}")
        lines.append("")

    opinions = research.get("expert_opinions") or []
    if opinions:
        lines.extend(["## Expert Opinions", ""])
        for item in opinions:
            lines.append(f"- {item}")
        lines.append("")

    conclusion = research.get("conclusion", "")
    if conclusion:
        lines.extend(["## Conclusion", "", conclusion, ""])

    sources = research.get("sources") or []
    if sources:
        lines.extend(["## Sources & References", ""])
        for index, source in enumerate(sources, start=1):
            title = source.get("title", "Untitled")
            url = source.get("url", "")
            date = source.get("date", "Unknown date")
            if url:
                lines.append(f"{index}. [{title}]({url}) — *{date}*")
            else:
                lines.append(f"{index}. **{title}** — *{date}*")
        lines.append("")

    generated_at = research.get("generated_at", "")
    if generated_at:
        lines.append(f"*Generated at: {generated_at}*")

    return "\n".join(lines)


def get_markdown_download(research: dict[str, Any]) -> tuple[bytes, str]:
    content = build_markdown_report(research)
    filename = _safe_filename(research.get("topic", "research"))
    return content.encode("utf-8"), filename
