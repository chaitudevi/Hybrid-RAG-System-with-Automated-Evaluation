from generation.generator import Generator

class LLMJudge:
    def __init__(self, config_path="../config.yaml"):
        self.generator = Generator(config_path)
        
    def evaluate(self, question, ground_truth, model_answer):
        prompt = f"""
        You are an impartial judge. Evaluate the quality of the answer provided by an AI assistant.
        
        Question: {question}
        Ground Truth: {ground_truth}
        Predicted Answer: {model_answer}
        
        Rate the answer on a scale of 1 to 5 for Factual Correctness.
        Output ONLY the number.
        """
        
        # We misuse the text2text generator here for judging
        # In production, use a separate, stronger model (e.g. GPT-4)
        try:
            rating = self.generator.pipe(prompt)[0]["generated_text"]
            # Extract number
            import re
            match = re.search(r"\d", rating)
            if match:
                return int(match.group())
            return 3 # Default fallback
        except:
            return 3

if __name__ == "__main__":
    judge = LLMJudge()
    print(judge.evaluate("Q", "A", "A"))
