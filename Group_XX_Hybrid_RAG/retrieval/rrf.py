def reciprocal_rank_fusion(dense_results, sparse_results, k=60):
    """
    Implements RRF fusion.
    dense_results: list of {chunk_id, score}
    sparse_results: list of {chunk_id, score}
    k: RRF constant
    """
    
    # Map chunk_id to RRF score
    scores = {}
    
    # Process Dense
    for rank, res in enumerate(dense_results):
        chunk_id = res["chunk_id"]
        if chunk_id not in scores:
            scores[chunk_id] = 0
        scores[chunk_id] += 1 / (k + rank + 1)
        
    # Process Sparse
    for rank, res in enumerate(sparse_results):
        chunk_id = res["chunk_id"]
        if chunk_id not in scores:
            scores[chunk_id] = 0
        scores[chunk_id] += 1 / (k + rank + 1)
        
    # Sort by score descending
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return list of {chunk_id, score}
    final_results = [{"chunk_id": item[0], "score": item[1]} for item in sorted_scores]
    return final_results
