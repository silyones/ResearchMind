import streamlit as st
import httpx
from datetime import datetime


def render_research_page(session_id: str) -> None:
    """
    Render the main research page with topic input and results display.
    
    Args:
        session_id: Current session identifier
    """
    st.header("🔍 Research")
    
    # Research input section
    col1, col2 = st.columns([4, 1])
    
    with col1:
        topic = st.text_input(
            "Enter a research topic",
            placeholder="e.g., 'Quantum Computing Breakthroughs in 2024'",
            help="Enter any topic you'd like to research",
        )
    
    with col2:
        search_button = st.button("🔎 Research", use_container_width=True)
    
    # Process research request
    if search_button and topic:
        st.session_state.current_topic = topic
        
        try:
            with st.spinner("🔄 Conducting research... This may take a minute."):
                # Call backend API
                response = httpx.post(
                    "http://localhost:8000/research",
                    json={"topic": topic},
                    params={"session_id": session_id},
                    timeout=300,  # 5 minutes timeout for long research
                )
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("success") and result.get("data"):
                    st.session_state.last_research = result["data"]
                    st.success("✅ Research completed!")
                else:
                    st.error(f"❌ Research failed: {result.get('error', 'Unknown error')}")
        
        except httpx.ConnectError:
            st.error("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        except httpx.TimeoutException:
            st.error("⏱️ Research took too long. Try a simpler topic.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Display research results
    if hasattr(st.session_state, "last_research") and st.session_state.last_research:
        research = st.session_state.last_research
        
        # Title and overview
        st.header(research.get("topic", "Research Results"))
        st.write(research.get("overview", ""))
        
        # Key Findings
        if research.get("key_findings"):
            with st.expander("📌 Key Findings", expanded=True):
                for i, finding in enumerate(research["key_findings"], 1):
                    st.write(f"**{i}. {finding.get('finding', '')}**")
                    source_url = finding.get("source_url", "")
                    if source_url:
                        st.caption(f"Source: [{source_url}]({source_url})")
        
        # Controversies
        if research.get("controversies"):
            with st.expander("⚖️ Controversies & Debates"):
                for controversy in research["controversies"]:
                    st.write(f"• {controversy}")
        
        # Expert Opinions
        if research.get("expert_opinions"):
            with st.expander("👨‍🎓 Expert Opinions"):
                for opinion in research["expert_opinions"]:
                    st.write(f"• {opinion}")
        
        # Conclusion
        if research.get("conclusion"):
            st.subheader("💡 Conclusion")
            st.write(research["conclusion"])
        
        # Sources
        if research.get("sources"):
            with st.expander("📚 Sources"):
                for i, source in enumerate(research["sources"], 1):
                    title = source.get("title", "Untitled")
                    url = source.get("url", "")
                    date = source.get("date", "Unknown date")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{i}. {title}**")
                        st.caption(f"Date: {date}")
                    with col2:
                        if url:
                            st.write(f"[🔗 Link]({url})")
        
        # Metadata
        generated_at = research.get("generated_at", "")
        if generated_at:
            st.divider()
            st.caption(f"Generated at: {generated_at}")
            st.caption(f"Session: `{session_id}`")
    
    elif not topic and search_button:
        st.warning("⚠️ Please enter a topic to research")
