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
            "ResearchMind helps you research any topic with AI. "
            "It searches the web, analyzes sources, and builds structured reports "
            "with key findings and references. "
            "You can read results in the app or download them as PDF or Markdown."
        )

        with st.expander("Developer links"):
            st.markdown("[Backend API](http://localhost:8000)")
            st.markdown("[API Docs](http://localhost:8000/docs)")
