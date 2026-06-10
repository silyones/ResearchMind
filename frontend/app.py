import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.pages.research import render_research_page


def main():
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="ResearchMind",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "last_research" not in st.session_state:
        st.session_state.last_research = None

    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""

    render_sidebar()
    render_research_page()


if __name__ == "__main__":
    main()
