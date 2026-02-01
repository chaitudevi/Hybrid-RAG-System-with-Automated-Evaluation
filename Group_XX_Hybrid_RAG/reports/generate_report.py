import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

def generate_report():
    input_dir = "../data/evaluation"
    output_dir = "../reports/figures"
    os.makedirs(output_dir, exist_ok=True)
    
    results_path = f"{input_dir}/results.csv"
    if not os.path.exists(results_path):
        print("No evaluation results found. Run evaluation pipeline first.")
        return

    df = pd.read_csv(results_path)
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # 1. MRR Comparison
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="mode", y="mrr", errorbar="sd")
    plt.title("MRR by Retrieval Strategy")
    plt.savefig(f"{output_dir}/mrr_comparison.png")
    print(f"Saved {output_dir}/mrr_comparison.png")
    
    # 2. Recall@5 Comparison
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="mode", y="recall_at_5", errorbar="sd")
    plt.title("Recall@5 by Retrieval Strategy")
    plt.savefig(f"{output_dir}/recall_comparison.png")
    print(f"Saved {output_dir}/recall_comparison.png")

if __name__ == "__main__":
    generate_report()
