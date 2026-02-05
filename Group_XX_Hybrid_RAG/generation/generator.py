from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import yaml
# Fix imports for running as script vs module
try:
    from generation.prompt_templates import QA_PROMPT
except ImportError:
    from prompt_templates import QA_PROMPT

class Generator:
    def __init__(self, config_path="../config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        model_name = self.config.get("llm_model", "google/flan-t5-base")
        print(f"Loading LLM {model_name}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
    def generate(self, query, retrieved_chunks):
        # Format context
        context_text = "\n\n".join([c["text"] for c in retrieved_chunks])
        
        prompt = QA_PROMPT.format(question=query, context=context_text)
        
        # Tokenize inputs
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        )
        
        # Greedy decoding for deterministic results
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=100,
            do_sample=False,  # Disable sampling to reduce hallucination
            temperature=0.0   # Enforce deterministic behavior
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    gen = Generator()
    print(gen.generate("What is AI?", [{"text": "AI stands for Artificial Intelligence."}]))
