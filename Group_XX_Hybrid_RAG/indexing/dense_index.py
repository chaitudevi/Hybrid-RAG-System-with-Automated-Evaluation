import json
import os
import yaml
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle

def load_config():
    with open("../config.yaml", "r") as f:
        return yaml.safe_load(f)

def build_dense_index():
    config = load_config()
    model_name = config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
    
    input_path = "../data/processed/chunks.jsonl"
    index_path = "../data/processed/dense.index"
    metadata_path = "../data/processed/dense_metadata.pkl"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print(f"Loading Embedding Model {model_name}...")
    model = SentenceTransformer(model_name)
    
    chunks = []
    chunk_ids = []
    
    print("Loading chunks...")
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            chunks.append(data["text"])
            chunk_ids.append(data["chunk_id"])
            
    print(f"Encoding {len(chunks)} chunks...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    
    print("Building FAISS index...")
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d) # Inner product for cosine similarity (normalized vectors)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    print(f"Saving index to {index_path}...")
    faiss.write_index(index, index_path)
    
    print(f"Saving metadata map to {metadata_path}...")
    with open(metadata_path, 'wb') as f:
        pickle.dump(chunk_ids, f)
        
    print("Dense indexing complete.")

if __name__ == "__main__":
    build_dense_index()
