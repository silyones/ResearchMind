import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.pages.research import render_research_page
from frontend.pages.history import render_history_page


def main():
    """Main Streamlit application entry point."""
    # Configure page
    st.set_page_config(
        page_title="ResearchMind",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Initialize session state
    if "last_research" not in st.session_state:
        st.session_state.last_research = None
    
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""
    
    # Render sidebar and get session_id
    session_id = render_sidebar()
    
    # Main content area with tabs
    tab1, tab2 = st.tabs([" Research", " History"])
    
    with tab1:
        render_research_page(session_id)
    
    with tab2:
        render_history_page(session_id)


if __name__ == "__main__":
    main()
