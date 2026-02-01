import sys
import os
import yaml

# Add root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from retrieval.hybrid_retriever import HybridRetriever

def debug_retrieval(query):
    config_path = os.path.join(project_root, "config.yaml")
    retriever = HybridRetriever(config_path)
    
    print(f"Query: {query}")
    print("-" * 50)
    
    results = retriever.retrieve(query)
    
    for i, res in enumerate(results):
        print(f"Rank {i+1} | Score: {res['score']:.4f} | Chunk ID: {res['chunk_id']}")
        print(f"Text Preview: {res['text'][:200]}...")
        print("-" * 30)

if __name__ == "__main__":
    debug_retrieval("what is transformer?")
