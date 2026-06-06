import streamlit as st


def render_sidebar() -> str:
    """
    Render the sidebar with app title, session management, and controls.
    
    Returns:
        Current session_id
    """
    with st.sidebar:
        # App title
        st.title("ResearchMind 🔬")
        st.divider()
        
        # Session ID management
        st.subheader("Session")
        
        # Initialize session_id in session_state if not present
        if "session_id" not in st.session_state:
            st.session_state.session_id = "default"
        
        # Session ID input
        session_id = st.text_input(
            "Session ID",
            value=st.session_state.session_id,
            help="Unique identifier for your conversation. Use the same ID to continue previous conversations.",
        )
        
        # Update session_state
        st.session_state.session_id = session_id
        
        # Display current session ID
        st.caption(f"Current: `{session_id}`")
        
        st.divider()
        
        # Clear history button
        if st.button(" Clear History", use_container_width=True):
            st.session_state.clear_history = True
            st.success("History cleared for this session!")
        
        st.divider()
        
        # Info section
        st.subheader("About")
        st.caption(
            "ResearchMind uses AI to conduct comprehensive research on any topic. "
            "Powered by Groq, Tavily, and LangChain."
        )
        st.caption(" Backend: http://localhost:8000")
        st.caption(" API Docs: http://localhost:8000/docs")
    
    return session_id
