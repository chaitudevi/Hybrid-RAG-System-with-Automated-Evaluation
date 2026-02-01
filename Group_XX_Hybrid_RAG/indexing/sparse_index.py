import json
import os
import pickle
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

def build_sparse_index():
    # Download punkt if not present
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        nltk.download('punkt_tab')

    input_path = "../data/processed/chunks.jsonl"
    index_path = "../data/processed/sparse.pkl"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    corpus_chunks = []
    chunk_ids = []
    
    print("Loading chunks for Sparse Indexing...")
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            corpus_chunks.append(data["text"])
            chunk_ids.append(data["chunk_id"])
            
    print("Tokenizing corpus...")
    tokenized_corpus = [word_tokenize(doc.lower()) for doc in corpus_chunks]
    
    print("Building BM25 index...")
    bm25 = BM25Okapi(tokenized_corpus)
    
    print(f"Saving BM25 object to {index_path}...")
    with open(index_path, "wb") as f:
        pickle.dump({"bm25": bm25, "ids": chunk_ids}, f)
        
    print("Sparse indexing complete.")

if __name__ == "__main__":
    build_sparse_index()
