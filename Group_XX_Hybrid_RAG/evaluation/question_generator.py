import json
import random
import os
import sys
from tqdm import tqdm

# Ensure we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from generation.generator import Generator
from generation.prompt_templates import QG_PROMPT

def generate_questions():
    print("Initializing Question Generator (this uses the LLM)...")
    
    # Paths
    docs_path = os.path.join(project_root, "data", "processed", "chunks.jsonl")
    output_path = os.path.join(project_root, "data", "questions", "qa_100.json") # Updated output path
    config_path = os.path.join(project_root, "config.yaml")

    if not os.path.exists(docs_path):
        print("Chunks not found. Run indexing first.")
        return

    # Load all chunks
    chunks = []
    with open(docs_path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
            
    # Sample 100 chunks randomly to be the source of truth
    # Ensure we cover the "fixed" and "random" sets if possible
    selected_chunks = random.sample(chunks, min(len(chunks), 100))
    
    # Initialize Generator (we reuse the class but will bypass the specific QA prompt logic by using model directly or modifying class)
    # Actually, Generator class uses QA_PROMPT in generate(). We'll need access to underlying model or add a generic generate method.
    # Let's instantiate Generator and use its model/tokenizer directly for QG to keep it clean.
    gen_agent = Generator(config_path)
    
    questions = []
    question_types = ["factual", "inferential"] # Multi-hop is hard to gen from single chunk
    
    print("Generating 100 questions from corpus...")
    
    for i, chunk in enumerate(tqdm(selected_chunks)):
        q_type = random.choice(question_types)
        text_snippet = chunk["text"][:1000] # Truncate for prompt limit safety
        
        # Manually format prompt since Generator.generate() forces QA_PROMPT
        prompt = QG_PROMPT.format(q_type=q_type, text=text_snippet)
        
        # Generate
        inputs = gen_agent.tokenizer(prompt, return_tensors="pt")
        # Generate question
        outputs = gen_agent.model.generate(**inputs, max_new_tokens=50)
        generated_question = gen_agent.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Basic cleaning
        generated_question = generated_question.replace("Question:", "").strip()
        
        questions.append({
            "id": f"q_{i:03d}",
            "question": generated_question,
            "ground_truth_url": chunk["url"],
            "ground_truth_context": chunk["text"],
            "chunk_id": chunk["chunk_id"],
            "type": q_type
        })
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2)
        
    print(f"Saved {len(questions)} generated questions to {output_path}")

if __name__ == "__main__":
    generate_questions()
