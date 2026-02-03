# ui_agent.py

import streamlit as st
import requests

AGENT_URL = "http://127.0.0.1:8001/agent"

st.set_page_config(page_title="Agent Demo", layout="wide")
st.title(" AI Agent Orchestration Demo")

query = st.text_area(
    "Enter your question:",
    height=200,
    placeholder="Ask anything..."
)

if st.button("Run Agent"):
    if not query.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    AGENT_URL,
                    json={"query": query}
                )
                response.raise_for_status()
                result = response.json()

                # Agent Decision
                st.subheader(" Agent Decision")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Selected Tool", result["selected_tool"])
                with col2:
                    st.metric("Confidence", result["confidence"])

                st.markdown("### Score Breakdown")
                st.json(result["score"])


                # Final Output

                st.subheader(" Final Answer")
                st.write(result["tool_output"]["answer"])

            except Exception as e:
                st.error(f"Request failed: {e}")
