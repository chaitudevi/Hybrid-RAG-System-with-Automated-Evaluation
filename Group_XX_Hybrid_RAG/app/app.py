import streamlit as st
import sys
import os
import yaml

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retrieval.hybrid_retriever import HybridRetriever
from generation.generator import Generator

st.set_page_config(page_title="Hybrid RAG System", layout="wide")

@st.cache_resource
def load_components():
    # Get absolute path to project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    config_path = os.path.join(project_root, "config.yaml")
    
    retriever = HybridRetriever(config_path)
    generator = Generator(config_path)
    return retriever, generator

try:
    retriever, generator = load_components()
except Exception as e:
    st.error(f"Failed to load components. Run indexing first! Error: {e}")
    st.stop()

st.title("🤖 Enterprise Hybrid RAG")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    st.write("Using Hybrid Retrieval (Dense + Sparse + RRF)")
    
    # Get absolute path to project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    config_path = os.path.join(project_root, "config.yaml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    st.json(config)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieval
            retrieved_chunks = retriever.retrieve(prompt)
            
            # Generation
            response = generator.generate(prompt, retrieved_chunks)
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Show sources in expander
            with st.expander("🔍 Retrieved Context (Evidence)"):
                for i, chunk in enumerate(retrieved_chunks):
                    st.markdown(f"**Source {i+1}** (Score: {chunk['score']:.4f})")
                    st.info(chunk["text"])
                    st.caption(f"URL: {chunk['url']}")
