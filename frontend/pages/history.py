import streamlit as st
import httpx


def render_history_page(session_id: str) -> None:
    """
    Render the conversation history page.
    
    Args:
        session_id: Current session identifier
    """
    st.header("📜 Conversation History")
    
    st.caption(f"Session: `{session_id}`")
    
    try:
        # Fetch history from backend
        response = httpx.get(
            f"http://localhost:8000/history/{session_id}",
            timeout=60,
        )
        response.raise_for_status()
        
        result = response.json()
        history = result.get("history", [])
        
        if not history:
            st.info("No conversation history yet. Start a research to begin!")
        else:
            st.write(f"**Total exchanges:** {len(history)}")
            st.divider()
            
            # Display conversation history
            for i, exchange in enumerate(history, 1):
                role = exchange.get("role", "unknown").title()
                content = exchange.get("content", "")
                
                # Style based on role
                if exchange.get("role") == "user":
                    with st.chat_message("user"):
                        st.write(content)
                elif exchange.get("role") == "assistant":
                    with st.chat_message("assistant"):
                        # Try to parse as JSON for formatted display
                        try:
                            import json
                            data = json.loads(content)
                            if isinstance(data, dict) and "topic" in data:
                                st.write(f"**Topic:** {data.get('topic', '')}")
                                st.write(f"**Overview:** {data.get('overview', '')[:200]}...")
                            else:
                                st.write(content)
                        except:
                            # If not JSON, display as plain text
                            st.write(content)
                else:
                    st.write(f"**{role}:** {content}")
                
                st.divider()
    
    except httpx.ConnectError:
        st.error("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except Exception as e:
        st.error(f"❌ Error loading history: {str(e)}")
    
    # Export button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
