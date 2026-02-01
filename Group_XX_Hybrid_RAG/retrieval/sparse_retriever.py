import pickle
import yaml
import os
import nltk
from nltk.tokenize import word_tokenize
import numpy as np

class SparseRetriever:
    def __init__(self, config_path="../config.yaml"):
        # Ensure punkt is ready
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            nltk.download('punkt_tab')

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        index_path = os.path.join(project_root, "data", "processed", "sparse.pkl")
        
        with open(index_path, "rb") as f:
            data = pickle.load(f)
            self.bm25 = data["bm25"]
            self.chunk_ids = data["ids"]
            
    def search(self, query, top_k=None):
        if top_k is None:
            top_k = self.config["sparse_top_k"]
            
        tokenized_query = word_tokenize(query.lower())
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top_k indices
        top_n = np.argsort(scores)[::-1][:top_k]
        
        results = []
        
        for idx in top_n:
            results.append({
                "chunk_id": self.chunk_ids[idx],
                "score": float(scores[idx])
            })
            
        return results

if __name__ == "__main__":
    sr = SparseRetriever()
    print(sr.search("Transformer architecture"))
