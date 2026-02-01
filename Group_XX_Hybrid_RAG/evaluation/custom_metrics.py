from rouge_score import rouge_scorer

def compute_rouge_score(prediction, reference):
    """
    Computes ROUGE-L score.
    """
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference, prediction)
    return scores['rougeL'].fmeasure

def compute_recall_at_k(retrieved_results, relevant_urls, k):
    """
    Recall@K: Is at least one relevant URL in the top K?
    """
    retrieved_urls = [r.get("url") for r in retrieved_results[:k]]
    # Handle single string relevant_url or list
    if isinstance(relevant_urls, str):
        relevant_urls = [relevant_urls]
        
    for url in relevant_urls:
        if url in retrieved_urls:
            return 1.0
    return 0.0

def compute_precision_at_k(retrieved_results, relevant_urls, k):
    """
    Precision@K: What fraction of top K are relevant?
    """
    retrieved_urls = [r.get("url") for r in retrieved_results[:k]]
    if isinstance(relevant_urls, str):
        relevant_urls = [relevant_urls]
        
    relevant_count = sum(1 for url in retrieved_urls if url in relevant_urls)
    return relevant_count / k if k > 0 else 0.0
