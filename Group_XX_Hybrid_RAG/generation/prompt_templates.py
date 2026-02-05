QA_PROMPT = """You are a helpful and strict assistant. Your goal is to answer the question using ONLY the provided context.
If the answer is not contained in the context, strictly say "I cannot answer this based on the provided context." Do not make up information.

Context:
{context}

Question: {question}

Answer:"""

QG_PROMPT = """Generate a {q_type} question based on the following text.
Text: {text}

Question:"""
