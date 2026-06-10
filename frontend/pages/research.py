import streamlit as st
import httpx
import json

from frontend.utils.pdf_export import generate_research_pdf


def _status_message(text: str) -> None:
    st.markdown(
        f'<p style="color:#21c354;margin:0.25rem 0 0;font-size:0.875rem;">{text}</p>',
        unsafe_allow_html=True,
    )


def _render_report(research: dict, session_id: str) -> None:
    topic = research.get("topic", "Research Results")

    header_col, download_col = st.columns([4, 1])
    with header_col:
        st.header(topic)
    with download_col:
        try:
            pdf_bytes, pdf_name = generate_research_pdf(research)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=pdf_name,
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as error:
            st.caption(f"PDF unavailable: {error}")

    overview = research.get("overview", "")
    if overview:
        st.markdown(f"*{overview}*")

    report = research.get("report", "")
    if report:
        st.markdown("---")
        st.subheader("Research Report")
        st.markdown(report)
    elif research.get("key_findings"):
        st.markdown("---")
        st.subheader("Research Report")
        for index, finding in enumerate(research["key_findings"], start=1):
            st.markdown(f"**{index}.** {finding.get('finding', '')}")

    if research.get("controversies"):
        st.subheader("Controversies & Debates")
        for controversy in research["controversies"]:
            st.markdown(f"- {controversy}")

    if research.get("expert_opinions"):
        st.subheader("Expert Opinions")
        for opinion in research["expert_opinions"]:
            st.markdown(f"- {opinion}")

    if report and research.get("key_findings"):
        with st.expander("Key Findings (Detailed)", expanded=False):
            for index, finding in enumerate(research["key_findings"], start=1):
                st.markdown(f"**{index}.** {finding.get('finding', '')}")

    conclusion = research.get("conclusion", "")
    if conclusion:
        st.markdown("---")
        st.subheader("Conclusion")
        st.markdown(conclusion)

    sources = research.get("sources") or []
    if sources:
        st.markdown("---")
        st.subheader("Sources & References")
        for index, source in enumerate(sources, start=1):
            title = source.get("title", "Untitled")
            url = source.get("url", "")
            date = source.get("date", "Unknown date")
            if url:
                st.markdown(f"{index}. [{title}]({url}) — *{date}*")
            else:
                st.markdown(f"{index}. **{title}** — *{date}*")

    generated_at = research.get("generated_at", "")
    if generated_at:
        st.divider()
        st.caption(f"Generated at: {generated_at}")
        st.caption(f"Session: `{session_id}`")


def render_research_page(session_id: str) -> None:
    st.header("Research")

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        topic = st.text_input(
            "Enter a research topic",
            placeholder="e.g., 'Quantum Computing Breakthroughs in 2026'",
        )

    with col2:
        st.markdown("<div style='height: 1.75rem'></div>", unsafe_allow_html=True)
        search_button = st.button("Research", use_container_width=True)

    with col3:
        st.markdown("<div style='height: 1.75rem'></div>", unsafe_allow_html=True)
        stream_button = st.button("Stream", use_container_width=True)

    if search_button and topic:
        st.session_state.last_research = None
        st.session_state.current_topic = topic
        st.session_state.research_status_message = None

        try:
            with st.spinner("Conducting research... This may take a minute."):
                response = httpx.post(
                    "http://localhost:8000/research",
                    json={"topic": topic},
                    params={"session_id": session_id},
                    timeout=300,
                )
                response.raise_for_status()
                result = response.json()

                if result.get("success") and result.get("data"):
                    st.session_state.last_research = result["data"]
                    st.session_state.research_status_message = "Research completed!"
                else:
                    st.error(f"Research failed: {result.get('error', 'Unknown error')}")

        except httpx.ConnectError:
            st.error("Cannot connect to backend. Make sure it's running on http://localhost:8000")
        except httpx.TimeoutException:
            st.error("Research took too long. Try a simpler topic.")
        except Exception as error:
            st.error(f"Error: {error}")

    if stream_button and topic:
        st.session_state.last_research = None
        st.session_state.current_topic = topic
        st.session_state.research_status_message = None

        try:
            status_placeholder = st.empty()
            stream_placeholder = st.empty()
            accumulated_text = ""

            with httpx.stream(
                "POST",
                "http://localhost:8000/research/stream",
                json={"topic": topic},
                params={"session_id": session_id},
                timeout=300,
            ) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line.startswith("data: "):
                            chunk = line.replace("data: ", "").strip()

                            if chunk == "[DONE]":
                                break
                            if chunk.startswith("[ERROR]"):
                                st.error(chunk)
                                break

                            accumulated_text += chunk
                            status_placeholder.info("Receiving research data...")

                    status_placeholder.empty()
                    stream_placeholder.empty()

                    try:
                        clean_text = accumulated_text.strip()
                        json_start = clean_text.find("{")
                        if json_start != -1:
                            clean_text = clean_text[json_start:]
                        research_data = json.loads(clean_text)
                        st.session_state.last_research = research_data
                        st.session_state.research_status_message = "Research completed!"
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
            _status_message(st.session_state.research_status_message)

    if st.session_state.get("last_research"):
        st.divider()
        _render_report(st.session_state.last_research, session_id)
    elif not topic and (search_button or stream_button):
        st.warning("Please enter a topic to research")
