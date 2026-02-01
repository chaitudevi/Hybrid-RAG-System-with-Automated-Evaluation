from retrieval.hybrid_retriever import HybridRetriever
from evaluation.mrr import compute_mrr
from evaluation.custom_metrics import compute_recall_at_k, compute_rouge_score, compute_precision_at_k
from generation.generator import Generator 
import pandas as pd
import json
import os
import sys

class AblationStudy:
    def __init__(self, config_path=None):
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, ".."))
            config_path = os.path.join(project_root, "config.yaml")
            
        self.retriever = HybridRetriever(config_path)
        self.generator = Generator(config_path)
        
    def run_ablation(self, questions, mode="hybrid"):
        results = []
        
        print(f"Running ablation for mode: {mode}")
        for q in questions:
            query = q["question"]
            gold_url = q["ground_truth_url"]
            gold_answer = q.get("ground_truth_context", "Not enough information")
            
            hits = []
            if mode == "dense":
                hits = self.retriever.dense.search(query)
            elif mode == "sparse":
                hits = self.retriever.sparse.search(query)
            elif mode == "hybrid":
                hits = self.retriever.retrieve(query)

            # Normalize hits to have URL for metric computation
            enriched_hits = []
            for hit in hits:
                if "url" in hit:
                    enriched_hits.append(hit)
                else:
                    # Look up URL from chunk_id
                    chunk_data = self.retriever.chunk_map.get(hit["chunk_id"])
                    if chunk_data:
                        hit["url"] = chunk_data["url"]
                        hit["text"] = chunk_data["text"]
                        enriched_hits.append(hit)
            
            # Metrics
            mrr = compute_mrr(enriched_hits, gold_url)
            recall = compute_recall_at_k(enriched_hits, gold_url, k=5)
            precision = compute_precision_at_k(enriched_hits, gold_url, k=5)
            
            # Generation & ROUGE
            model_answer = "Not enough information"
            if enriched_hits:
                try:
                    # Handle different return formats from retrievers
                    model_answer = self.generator.generate(query, enriched_hits)
                except Exception as e:
                    print(f"Error generating answer: {e}")
            
            rouge = compute_rouge_score(model_answer, gold_answer)
            
            results.append({
                "question_id": q["id"],
                "mode": mode,
                "mrr": mrr,
                "recall_at_5": recall,
                "precision_at_5": precision,
                "rouge_l": rouge,
                "generated_answer": model_answer,
                "ground_truth_answer": gold_answer
            })
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    # Test run
    pass
