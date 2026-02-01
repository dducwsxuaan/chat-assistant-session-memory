import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.memory_manager import MemoryManager
from core.query_processor import QueryProcessor
from graph.builder import build_graph

st.set_page_config(page_title="LangGraph Assistant", page_icon="🤖")


if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager(threshold=300)
    st.session_state.processor = QueryProcessor(st.session_state.memory)
    st.session_state.graph = build_graph()
    st.session_state.chat_history = []
    st.session_state.messages = []

st.title("🤖 Chat Assistant with Session Memory")

user_input = st.chat_input("Type your message...")

if user_input:
    
    

    with st.chat_message("user"):
        st.write(user_input)

    
    state = {
        "user_query": user_input,
        "mm": st.session_state.memory,
        "qp": st.session_state.processor,
        "debug": False
    }

    result = st.session_state.graph.invoke(state)

    assistant_reply = result.get(
        "assistant_output",
        "⚠️ No response generated."
    )

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    
    with st.chat_message("assistant"):
        st.write(assistant_reply)
