import yaml
import json
import os
# Fix imports for running as script vs module
try:
    from retrieval.dense_retriever import DenseRetriever
    from retrieval.sparse_retriever import SparseRetriever
    from retrieval.rrf import reciprocal_rank_fusion
except ImportError:
    from dense_retriever import DenseRetriever
    from sparse_retriever import SparseRetriever
    from rrf import reciprocal_rank_fusion

class HybridRetriever:
    def __init__(self, config_path="../config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.dense = DenseRetriever(config_path)
        self.sparse = SparseRetriever(config_path)
        
        # Load chunks to return text
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        chunks_path = os.path.join(project_root, "data", "processed", "chunks.jsonl")
        
        self.chunk_map = {}
        with open(chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                self.chunk_map[data["chunk_id"]] = data
                
    def retrieve(self, query):
        dense_hits = self.dense.search(query, top_k=self.config["dense_top_k"])
        sparse_hits = self.sparse.search(query, top_k=self.config["sparse_top_k"])
        
        # RRF Fusion
        rrf_hits = reciprocal_rank_fusion(
            dense_hits, 
            sparse_hits, 
            k=self.config.get("rrf_k", 60)
        )
        
        # Get top N final context
        top_n = self.config.get("final_context_n", 5)
        final_hits = rrf_hits[:top_n]
        
        # Enrich with text
        results = []
        for hit in final_hits:
            chunk_data = self.chunk_map.get(hit["chunk_id"])
            if chunk_data:
                results.append({
                    "chunk_id": hit["chunk_id"],
                    "score": hit["score"],
                    "text": chunk_data["text"],
                    "url": chunk_data["url"],
                    "source": chunk_data["source"]
                })
                
        return results

if __name__ == "__main__":
    hr = HybridRetriever()
    results = hr.retrieve("What is a Transformer?")
    for res in results:
        print(f"[{res['score']:.4f}] {res['chunk_id']} - {res['text'][:50]}...")
