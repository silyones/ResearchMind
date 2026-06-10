import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.pages.research import render_research_page
from frontend.utils.ui import inject_styles


def main():
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="Research Mind",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_styles()

    if "last_research" not in st.session_state:
        st.session_state.last_research = None

    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""

    if "research_topic" not in st.session_state:
        st.session_state.research_topic = ""

    if "research_started" not in st.session_state:
        st.session_state.research_started = False

    if "research_in_progress" not in st.session_state:
        st.session_state.research_in_progress = False

    if "show_example_ui" not in st.session_state:
        st.session_state.show_example_ui = True

    if "example_widget_generation" not in st.session_state:
        st.session_state.example_widget_generation = 0

    render_sidebar()
    render_research_page()


if __name__ == "__main__":
    main()
