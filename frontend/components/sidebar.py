import streamlit as st


def render_sidebar() -> None:
    """Render the sidebar with app title and info."""
    with st.sidebar:
        st.markdown('<p class="rm-sidebar-title">Research Mind</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="rm-badge-row">
                <span class="rm-badge">Groq</span>
                <span class="rm-badge">Tavily</span>
                <span class="rm-badge">LangChain</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        st.subheader("About")
        st.caption(
            "ResearchMind uses AI to conduct comprehensive research on any topic — "
            "from quick summaries to full downloadable reports."
        )

        with st.expander("Developer links"):
            st.markdown("[Backend API](http://localhost:8000)")
            st.markdown("[API Docs](http://localhost:8000/docs)")
