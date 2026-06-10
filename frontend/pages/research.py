import json
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import streamlit as st

from frontend.utils.pdf_export import generate_research_pdf
from frontend.utils.report_export import get_markdown_download
from frontend.utils.ui import (
    LOADING_STEPS,
    render_card,
    render_example_topics,
    render_finding,
    render_hero,
    render_metadata_bar,
    status_message,
)


def _render_report(research: dict) -> None:
    topic = research.get("topic", "Research Results")

    header_col, pdf_col, md_col = st.columns([3, 1, 1])
    with header_col:
        st.header(topic)
    with pdf_col:
        try:
            pdf_bytes, pdf_name = generate_research_pdf(research)
            st.download_button(
                label="📄 PDF",
                data=pdf_bytes,
                file_name=pdf_name,
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as error:
            st.caption(f"PDF unavailable: {error}")
    with md_col:
        md_bytes, md_name = get_markdown_download(research)
        st.download_button(
            label="📝 Markdown",
            data=md_bytes,
            file_name=md_name,
            mime="text/markdown",
            use_container_width=True,
        )

    render_metadata_bar(research)

    overview = research.get("overview", "")
    if overview:
        render_card("Executive Summary", overview, extra_class="rm-summary")

    report = research.get("report", "")
    if report:
        st.subheader("Research Report")
        st.markdown(report)
    elif research.get("key_findings"):
        st.subheader("Research Report")
        for index, finding in enumerate(research["key_findings"], start=1):
            render_finding(index, finding.get("finding", ""))

    if research.get("key_findings") and report:
        with st.expander("Key Findings", expanded=False):
            for index, finding in enumerate(research["key_findings"], start=1):
                render_finding(index, finding.get("finding", ""))

    if research.get("controversies"):
        with st.expander("Controversies & Debates", expanded=False):
            for controversy in research["controversies"]:
                st.markdown(f"- {controversy}")

    if research.get("expert_opinions"):
        with st.expander("Expert Opinions", expanded=False):
            for opinion in research["expert_opinions"]:
                st.markdown(f"- {opinion}")

    conclusion = research.get("conclusion", "")
    if conclusion:
        st.subheader("Conclusion")
        render_card("Synthesis", conclusion)

    sources = research.get("sources") or []
    if sources:
        st.subheader("Sources & References")
        st.markdown('<div class="rm-sources">', unsafe_allow_html=True)
        for index, source in enumerate(sources, start=1):
            title = source.get("title", "Untitled")
            url = source.get("url", "")
            date = source.get("date", "Unknown date")
            if url:
                st.markdown(f"{index}. [{title}]({url}) — *{date}*")
            else:
                st.markdown(f"{index}. **{title}** — *{date}*")
        st.markdown("</div>", unsafe_allow_html=True)


def _run_with_loading_steps(request_fn):
    """Show step-by-step progress while a blocking request runs."""
    with st.status("Research in progress…", expanded=True) as status:
        progress = st.empty()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(request_fn)
            step_index = 0
            while not future.done():
                progress.write(LOADING_STEPS[step_index % len(LOADING_STEPS)])
                time.sleep(0.6)
                step_index += 1
            result = future.result()
        status.update(label="Research complete!", state="complete", expanded=False)
    return result


def _conduct_research(topic: str) -> None:
    st.session_state.last_research = None
    st.session_state.current_topic = topic
    st.session_state.research_status_message = None

    try:

        def do_research():
            response = httpx.post(
                "http://localhost:8000/research",
                json={"topic": topic},
                timeout=300,
            )
            response.raise_for_status()
            return response.json()

        result = _run_with_loading_steps(do_research)

        if result.get("success") and result.get("data"):
            st.session_state.last_research = result["data"]
            st.session_state.research_status_message = "Research completed!"
        else:
            st.session_state.selected_example = None
            st.error(f"Research failed: {result.get('error', 'Unknown error')}")

    except httpx.ConnectError:
        st.session_state.selected_example = None
        st.error("Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except httpx.TimeoutException:
        st.session_state.selected_example = None
        st.error("Research took too long. Try a simpler topic.")
    except Exception as error:
        st.session_state.selected_example = None
        st.error(f"Error: {error}")


def render_research_page() -> None:
    show_hero = not st.session_state.get("last_research")
    if show_hero:
        render_hero()

    st.header("Research")

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        topic = st.text_input(
            "Enter a research topic",
            placeholder="e.g., 'Quantum Computing Breakthroughs in 2026'",
            key="research_topic",
        )

    with col2:
        st.markdown("<div style='height: 1.75rem'></div>", unsafe_allow_html=True)
        search_button = st.button("🔍 Research", use_container_width=True, type="primary")

    with col3:
        st.markdown("<div style='height: 1.75rem'></div>", unsafe_allow_html=True)
        stream_button = st.button("📡 Stream", use_container_width=True)

    st.caption("Research runs a full report · Stream shows live token output")

    if show_hero:
        render_example_topics()

    if search_button and topic:
        st.session_state.selected_example = None
        _conduct_research(topic)

    if st.session_state.pop("trigger_research", False) and topic:
        _conduct_research(topic)

    if stream_button and topic:
        st.session_state.last_research = None
        st.session_state.current_topic = topic
        st.session_state.research_status_message = None

        try:
            with st.status("Streaming research…", expanded=True) as status:
                st.write("Connecting to backend…")
                accumulated_text = ""

                with httpx.stream(
                    "POST",
                    "http://localhost:8000/research/stream",
                    json={"topic": topic},
                    timeout=300,
                ) as response:
                    if response.status_code == 200:
                        st.write("Receiving live output…")
                        for line in response.iter_lines():
                            if line.startswith("data: "):
                                chunk = line.replace("data: ", "").strip()

                                if chunk == "[DONE]":
                                    break
                                if chunk.startswith("[ERROR]"):
                                    st.error(chunk)
                                    break

                                accumulated_text += chunk

                        try:
                            clean_text = accumulated_text.strip()
                            json_start = clean_text.find("{")
                            if json_start != -1:
                                clean_text = clean_text[json_start:]
                            research_data = json.loads(clean_text)
                            st.session_state.last_research = research_data
                            st.session_state.research_status_message = "Research completed!"
                            status.update(
                                label="Research complete!",
                                state="complete",
                                expanded=False,
                            )
                        except json.JSONDecodeError:
                            st.warning("Could not parse research results.")
                    else:
                        st.error(f"Stream failed with status {response.status_code}")

        except httpx.ConnectError:
            st.error("Cannot connect to backend. Make sure it's running on http://localhost:8000")
        except Exception as error:
            st.error(f"Streaming error: {error}")

    if st.session_state.get("research_status_message"):
        msg_col, _, _ = st.columns([3, 1, 1])
        with msg_col:
            status_message(st.session_state.research_status_message)

    if st.session_state.get("last_research"):
        st.divider()
        _render_report(st.session_state.last_research)
    elif not topic and (search_button or stream_button):
        st.warning("Please enter a topic to research")
