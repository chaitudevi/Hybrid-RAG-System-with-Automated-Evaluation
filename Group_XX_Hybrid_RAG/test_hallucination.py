from generation.generator import Generator

def test_hallucination_fixes():
    gen = Generator(config_path="config.yaml")

    print("\n--- Test 1: Relevant Context ---")
    context1 = [{"text": "DeepMind was founded in London in 2010."}]
    query1 = "When was DeepMind founded?"
    response1 = gen.generate(query1, context1)
    print(f"Context: {context1[0]['text']}")
    print(f"Query: {query1}")
    print(f"Response: {response1}")
    
    print("\n--- Test 2: Irrelevant Context ---")
    context2 = [{"text": "The apple is a fruit."}]
    query2 = "Who is the CEO of Google?"
    response2 = gen.generate(query2, context2)
    print(f"Context: {context2[0]['text']}")
    print(f"Query: {query2}")
    print(f"Response: {response2}")
    
    # Expected behavior
    if "I cannot answer this" in response2 or "context" in response2.lower():
         print("\nSUCCESS: Model correctly refused to answer based on missing context.")
    else:
         print("\nFAILURE: Model hallucinated an answer.")

if __name__ == "__main__":
    test_hallucination_fixes()
