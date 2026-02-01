import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import yaml
import os

class DenseRetriever:
    def __init__(self, config_path="../config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.model_name = self.config["embedding_model"]
        self.model = SentenceTransformer(self.model_name)
        
        # Get absolute path to data directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        
        index_path = os.path.join(project_root, "data", "processed", "dense.index")
        metadata_path = os.path.join(project_root, "data", "processed", "dense_metadata.pkl")

        self.index = faiss.read_index(index_path)
        with open(metadata_path, 'rb') as f:
            self.chunk_ids = pickle.load(f)
            
    def search(self, query, top_k=None):
        if top_k is None:
            top_k = self.config["dense_top_k"]
            
        query_vector = self.model.encode([query]).astype("float32")
        faiss.normalize_L2(query_vector)
        
        scores, indices = self.index.search(query_vector, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append({
                    "chunk_id": self.chunk_ids[idx],
                    "score": float(score)
                })
        return results

if __name__ == "__main__":
    dr = DenseRetriever()
    print(dr.search("Transformer architecture"))
