import streamlit as st


def render_sidebar() -> None:
    """Render the sidebar with app title and info."""
    with st.sidebar:
        st.title("Research Mind")
        st.divider()

        st.subheader("About")
        st.caption(
            "ResearchMind uses AI to conduct comprehensive research on any topic. "
            "Powered by Groq, Tavily, and LangChain."
        )
        st.caption("Backend: http://localhost:8000")
        st.caption("API Docs: http://localhost:8000/docs")
