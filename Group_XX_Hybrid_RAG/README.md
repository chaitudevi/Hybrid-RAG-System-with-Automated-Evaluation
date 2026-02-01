# Group_XX Hybrid RAG System

 Industry-grade Hybrid RAG system combining Dense Retrieval, Sparse Retrieval (BM25), and Reciprocal Rank Fusion (RRF).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure parameters in `config.yaml`.

## Usage

### Indexing
Run the indexing pipeline to build the corpus and indexes:
```bash
./scripts/build_index.sh
```

### Application
Launch the Streamlit UI:
```bash
./scripts/run_app.sh
```

### Evaluation
Run the full evaluation suite:
```bash
./scripts/run_evaluation.sh
```

## Structure
- `data/`: Contains raw and processed data, including fixed/random URLs.
- `indexing/`: Modules for building the corpus and indexes.
- `retrieval/`: Dense, Sparse, and Hybrid retrieval logic.
- `generation/`: LLM generation and prompting.
- `evaluation/`: Metrics, question generation, and validation.
- `app/`: Streamlit web interface.
- `reports/`: Generated figures and tables.
