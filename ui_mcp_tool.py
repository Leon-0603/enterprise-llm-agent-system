# ui_mcp_tool.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/run"

st.set_page_config(page_title="MCP Demo", layout="wide")
st.title(" MCP Tool Demo — RAG / LoRA Inference")

# Select Tool
tool = st.selectbox(
    "Select Tool",
    ["rag_tool", "lora_tool"]
)

# Input Prompt
prompt = st.text_area(
    "Enter your question or prompt:",
    height=200,
    placeholder="Ask anything..."
)

# Run button
if st.button("Run Tool"):
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        payload = {
            "tool": tool,
            "params": {
                "query": prompt
            } if tool == "rag_tool" else {
                "prompt": prompt
            }
        }

        with st.spinner("Running..."):
            try:
                response = requests.post(API_URL, json=payload)
                result = response.json()

                st.subheader(" Output")
                
                # RAG OUTPUT
                if tool == "rag_tool":
                    answer = result.get("output", {}).get("answer")
                    st.write(answer)

                    chunks = result.get("output", {}).get("chunks", [])
                    if chunks:
                        st.subheader(" Retrieved Chunks")
                        for i, c in enumerate(chunks):
                            st.markdown(f"**[{i+1}] {c['title']} — page {c['page']}**")
                            st.write(c["content"])
                            st.write("---")

                # LORA OUTPUT
                elif tool == "lora_tool":
                    output = result.get("output")
                    st.write(output)

            except Exception as e:
                st.error(f"Request failed: {e}")
