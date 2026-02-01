def compute_mrr(retrieved_results, ground_truth_url):
    """
    Computes MRR based on whether the ground_truth_url is in the retrieved results.
    retrieved_results: list of dicts with 'url' key
    ground_truth_url: string
    """
    for rank, res in enumerate(retrieved_results):
        if res.get("url") == ground_truth_url:
            return 1.0 / (rank + 1)
    return 0.0
