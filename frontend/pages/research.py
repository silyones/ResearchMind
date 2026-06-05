import streamlit as st
import httpx
import json
from datetime import datetime


def render_research_page(session_id: str) -> None:
    st.header("🔍 Research")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        topic = st.text_input(
            "Enter a research topic",
            placeholder="e.g., 'Quantum Computing Breakthroughs in 2024'",
            help="Enter any topic you'd like to research",
        )
    
    with col2:
        search_button = st.button("🔎 Research", use_container_width=True)
    
    with col3:
        stream_button = st.button("📡 Stream", use_container_width=True)
    
    # Non-streaming research
    if search_button and topic:
        st.session_state.current_topic = topic
        
        try:
            with st.spinner("🔄 Conducting research... This may take a minute."):
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
                    st.success("✅ Research completed!")
                else:
                    st.error(f"❌ Research failed: {result.get('error', 'Unknown error')}")
        
        except httpx.ConnectError:
            st.error("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        except httpx.TimeoutException:
            st.error("⏱️ Research took too long. Try a simpler topic.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Streaming research
    if stream_button and topic:
        st.session_state.current_topic = topic
        
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
                            elif chunk.startswith("[ERROR]"):
                                st.error(f"❌ {chunk}")
                                break
                            else:
                                accumulated_text += chunk
                                # Show a simple progress message, not raw JSON
                                status_placeholder.info("📡 Receiving research data...")
                    
                    # Clear the progress message
                    status_placeholder.empty()
                    stream_placeholder.empty()
                    
                    # Parse and store result
                    try:
                        research_data = json.loads(accumulated_text)
                        st.session_state.last_research = research_data
                        st.success("✅ Research complete!")
                    except json.JSONDecodeError:
                        st.warning("⚠️ Could not parse research results.")
                else:
                    st.error(f"Stream failed with status {response.status_code}")
        
        except httpx.ConnectError:
            st.error("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        except Exception as e:
            st.error(f"❌ Streaming error: {str(e)}")
    
    # Display research results
    if hasattr(st.session_state, "last_research") and st.session_state.last_research:
        research = st.session_state.last_research
        
        st.divider()
        
        st.header(research.get("topic", "Research Results"))
        st.write(research.get("overview", ""))
        
        if research.get("key_findings"):
            with st.expander("📌 Key Findings", expanded=True):
                for i, finding in enumerate(research["key_findings"], 1):
                    st.write(f"**{i}. {finding.get('finding', '')}**")
                    source_url = finding.get("source_url", "")
                    if source_url:
                        st.caption(f"Source: [{source_url}]({source_url})")
        
        if research.get("controversies"):
            with st.expander("⚖️ Controversies & Debates"):
                for controversy in research["controversies"]:
                    st.write(f"• {controversy}")
        
        if research.get("expert_opinions"):
            with st.expander("👨‍🎓 Expert Opinions"):
                for opinion in research["expert_opinions"]:
                    st.write(f"• {opinion}")
        
        if research.get("conclusion"):
            st.subheader("💡 Conclusion")
            st.write(research["conclusion"])
        
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
        
        generated_at = research.get("generated_at", "")
        if generated_at:
            st.divider()
            st.caption(f"Generated at: {generated_at}")
            st.caption(f"Session: `{session_id}`")
    
    elif not topic and (search_button or stream_button):
        st.warning("⚠️ Please enter a topic to research")