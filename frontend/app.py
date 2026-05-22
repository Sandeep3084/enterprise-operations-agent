import streamlit as st
import requests

st.set_page_config(
    page_title="Enterprise Operations Agent",
    page_icon="💼",
    layout="centered"
)

st.title("💼 Autonomous Operations Engine")
st.caption("A multi-agent architecture featuring dynamic routing, semantic local RAG, and live tool execution.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your automated operations agent. I can track e-commerce order statuses, qualify inbound B2B sales leads, query our internal knowledge base, or run live web scraper crawls. How can I assist you today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question or issue a command..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent workflow executing..."):
            try:
                # Local test URL (switch this to your Render URL when deploying live)
                api_url = "http://127.0.0.1:8000/chat"
                
                payload = {"messages": st.session_state.messages}
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    agent_reply = response.json().get("response", "Error: Empty response body received.")
                    st.markdown(agent_reply)
                    st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Connection failed. Is the FastAPI backend running on port 8000?")