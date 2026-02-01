import json
import os
import yaml
from tqdm import tqdm
from transformers import AutoTokenizer

def load_config():
    with open("../config.yaml", "r") as f:
        return yaml.safe_load(f)

def chunk_text(text, tokenizer, chunk_size, chunk_overlap):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    
    for i in range(0, len(tokens), chunk_size - chunk_overlap):
        chunk_tokens = tokens[i : i + chunk_size]
        if len(chunk_tokens) < 50: # Skip very small chunks
            continue
            
        chunk_text_str = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text_str)
        
    return chunks

def process_documents():
    config = load_config()
    chunk_size = config.get("chunk_size", 300)
    chunk_overlap = config.get("chunk_overlap", 50)
    model_name = config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
    
    print(f"Loading Tokenizer {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    input_path = "../data/processed/documents.jsonl"
    output_path = "../data/processed/chunks.jsonl"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print("Chunking documents...")
    all_chunks = []
    
    with open(input_path, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            doc = json.loads(line)
            doc_id = doc["id"]
            text = doc["text"]
            
            chunks = chunk_text(text, tokenizer, chunk_size, chunk_overlap)
            
            for i, chunk_content in enumerate(chunks):
                chunk_data = {
                    "chunk_id": f"{doc_id}_chunk_{i:02d}",
                    "doc_id": doc_id,
                    "url": doc["url"],
                    "text": chunk_content,
                    "source": doc["source"]
                }
                all_chunks.append(chunk_data)
                
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")
            
    print(f"Saved {len(all_chunks)} chunks to {output_path}")

if __name__ == "__main__":
    process_documents()
