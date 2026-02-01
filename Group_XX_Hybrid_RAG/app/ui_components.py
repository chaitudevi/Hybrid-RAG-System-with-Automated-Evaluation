import streamlit as st

def display_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

def display_retrieved_chunk(i, chunk):
    st.markdown(f"**Source {i+1}** (Score: {chunk['score']:.4f})")
    st.info(chunk["text"])
    st.caption(f"URL: {chunk.get('url', 'N/A')}")
