import json
import os
import sys

# Ensure generation and retrieval modules are reachable
# Add path BEFORE imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from evaluation.ablation import AblationStudy
from evaluation.question_generator import generate_questions 

def run_pipeline():
    # Get absolute path to project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    # 1. Load or Generate Questions
    q_path = os.path.join(project_root, "data", "questions", "qa_100.json")
    if not os.path.exists(q_path):
        print("Generating questions...")
        generate_questions()
        
    with open(q_path, "r") as f:
        questions = json.load(f)
        
    print(f"Loaded {len(questions)} questions.")
    
    # 2. Run Ablation Studies
    study = AblationStudy()
    
    modes = ["dense", "sparse", "hybrid"]
    all_results = pd.DataFrame()
    
    for mode in modes:
        print(f"Running evaluation for mode: {mode}...")
        df = study.run_ablation(questions, mode)
        all_results = pd.concat([all_results, df])
        
    # 3. Save Results
    output_dir = os.path.join(project_root, "data", "evaluation")
    os.makedirs(output_dir, exist_ok=True)
    
    res_path = f"{output_dir}/results.csv"
    all_results.to_csv(res_path, index=False)
    print(f"Saved detailed results to {res_path}")
    
    # 4. Compute & Save Aggregate Metrics
    metrics_summary = {}
    for mode in modes:
        mode_df = all_results[all_results["mode"] == mode]
        # Check if columns exist (ablation might result in empty dataframe or missing columns if error)
        if not mode_df.empty:
            metrics_summary[mode] = {
                "mrr": float(mode_df["mrr"].mean()) if "mrr" in mode_df else 0.0,
                "recall_at_5": float(mode_df["recall_at_5"].mean()) if "recall_at_5" in mode_df else 0.0,
                "precision_at_5": float(mode_df["precision_at_5"].mean()) if "precision_at_5" in mode_df else 0.0,
                "rouge_l": float(mode_df["rouge_l"].mean()) if "rouge_l" in mode_df else 0.0,
            }
        
    metrics_path = os.path.join(output_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics_summary, f, indent=2)
        
    print(f"Saved aggregated metrics to {metrics_path}")
    print("\nEvaluation Summary:")
    print(json.dumps(metrics_summary, indent=2))

if __name__ == "__main__":
    # Ensure correct working directory if run from scripts
    if os.path.basename(os.getcwd()) != "Group_XX_Hybrid_RAG":
        # Attempt to find the root
        pass
    run_pipeline()
