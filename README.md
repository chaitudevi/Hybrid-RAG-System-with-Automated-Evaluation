# Hybrid RAG System with Automated Evaluation

This repository contains an industry-grade Hybrid RAG system combining Dense Retrieval, Sparse Retrieval (BM25), and Reciprocal Rank Fusion (RRF). It includes a Streamlit application and a comprehensive evaluation pipeline.

## Prerequisites

- Python 3.8 or higher
- Git

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chaitudevi/Hybrid-RAG-System-with-Automated-Evaluation.git
   cd Hybrid-RAG-System-with-Automated-Evaluation
   ```

2. **Create and activate a virtual environment:**

   *   **Windows:**
       ```powershell
       python -m venv .venv
       .venv\Scripts\activate
       ```
   *   **Linux/Mac:**
       ```bash
       python3 -m venv .venv
       source .venv/bin/activate
       ```

3. **Install dependencies:**
   ```bash
   pip install -r Group_XX_Hybrid_RAG/requirements.txt
   ```

4. **Configuration:**
   The system configuration is located in `Group_XX_Hybrid_RAG/config.yaml`. You can adjust parameters like model names, paths, and retrieval settings there.

## Usage

All scripts are located in `Group_XX_Hybrid_RAG/scripts/`.

### 1. Build Index
Run this first to generate the corpus (fixed + random URLs) and build the dense/sparse indexes.

*   **Windows:**
    ```powershell
    .\Group_XX_Hybrid_RAG\scripts\build_index.bat
    ```
*   **Linux/Mac:**
    ```bash
    ./Group_XX_Hybrid_RAG/scripts/build_index.sh
    ```

### 2. Run Application
Launch the Streamlit web interface to interact with the RAG system.

*   **Windows:**
    ```powershell
    .\Group_XX_Hybrid_RAG\scripts\run_app.bat
    ```
*   **Linux/Mac:**
    ```bash
    ./Group_XX_Hybrid_RAG/scripts/run_app.sh
    ```

### 3. Run Evaluation
Run the automated evaluation pipeline to assess retrieval and generation performance.

*   **Windows:**
    ```powershell
    .\Group_XX_Hybrid_RAG\scripts\run_evaluation.bat
    ```
*   **Linux/Mac:**
    ```bash
    ./Group_XX_Hybrid_RAG/scripts/run_evaluation.sh
    ```

## Project Structure

- `Group_XX_Hybrid_RAG/data/`: Raw and processed data.
- `Group_XX_Hybrid_RAG/indexing/`: Indexing logic (Dense, Sparse).
- `Group_XX_Hybrid_RAG/retrieval/`: Search implementations (Hybrid, RRF).
- `Group_XX_Hybrid_RAG/generation/`: LLM integration.
- `Group_XX_Hybrid_RAG/evaluation/`: Metrics and evaluation loop.
- `Group_XX_Hybrid_RAG/app/`: Streamlit UI code.
- `Group_XX_Hybrid_RAG/reports/`: Evaluation outputs.
