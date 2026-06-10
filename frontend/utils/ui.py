import html
from pathlib import Path

import streamlit as st

EXAMPLE_TOPICS = [
    "New models released by Claude.ai",
    "AI regulation updates worldwide",
    "Renewable energy trends",
]

LOADING_STEPS = [
    "Searching the web for sources…",
    "Analyzing and cross-checking findings…",
    "Writing your research report…",
]


def inject_styles() -> None:
    css_path = Path(__file__).resolve().parent.parent / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        """
        <div class="rm-hero">
            <p class="rm-hero-title">AI-powered research reports in seconds</p>
            <p class="rm-hero-subtitle">
                Enter any topic below. Research Mind searches the web, analyzes sources,
                and delivers a structured report you can read or download as PDF.
            </p>
            <div class="rm-steps-flow">
                <span class="rm-step-label"><strong>1.</strong> Search</span>
                <span class="rm-step-arrow" aria-hidden="true">→</span>
                <span class="rm-step-label"><strong>2.</strong> Analyze</span>
                <span class="rm-step-arrow" aria-hidden="true">→</span>
                <span class="rm-step-label"><strong>3.</strong> Report + PDF</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _start_example_research(topic: str) -> None:
    st.session_state.research_topic = topic
    st.session_state.research_started = True
    st.session_state.last_research = None
    st.session_state.research_status_message = None
    st.session_state.pending_research_topic = topic


def render_example_topics() -> None:
    st.caption("Try an example topic:")
    for index, topic in enumerate(EXAMPLE_TOPICS):
        st.button(
            topic,
            key=f"example_topic_{index}",
            on_click=_start_example_research,
            args=(topic,),
        )


def status_message(text: str) -> None:
    st.markdown(f'<p class="rm-status-ok">{text}</p>', unsafe_allow_html=True)


def render_card(title: str, body: str, extra_class: str = "") -> None:
    css_class = f"rm-card {extra_class}".strip()
    safe_body = html.escape(body).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="{css_class}">
            <p class="rm-card-title">{html.escape(title)}</p>
            <p class="rm-card-body">{safe_body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metadata_bar(research: dict) -> None:
    sources = research.get("sources") or []
    report = research.get("report", "") or research.get("overview", "")
    word_count = len(report.split())
    generated = research.get("generated_at", "—")
    if isinstance(generated, str) and "T" in generated:
        generated = generated.replace("T", " ").split(".")[0]

    st.markdown(
        f"""
        <div class="rm-meta">
            <div class="rm-meta-item">Sources<span>{len(sources)}</span></div>
            <div class="rm-meta-item">Words<span>{word_count:,}</span></div>
            <div class="rm-meta-item">Generated<span>{generated}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_finding(index: int, text: str) -> None:
    safe_text = html.escape(text)
    st.markdown(
        f"""
        <div class="rm-finding">
            <span class="rm-finding-num">{index}.</span>{safe_text}
        </div>
        """,
        unsafe_allow_html=True,
    )
