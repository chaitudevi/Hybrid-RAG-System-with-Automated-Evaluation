import subprocess
import os
import sys

def run_step(script_name):
    print(f"=== Running {script_name} ===")
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"Error running {script_name}")
        sys.exit(result.returncode)
        
def main():
    # Ensure execution from the indexing folder for relative paths
    if os.path.basename(os.getcwd()) != "indexing":
        try:
            os.chdir("indexing")
        except FileNotFoundError:
            if os.path.exists("Group_XX_Hybrid_RAG/indexing"):
                os.chdir("Group_XX_Hybrid_RAG/indexing")
    
    steps = [
        "build_corpus.py",
        "chunker.py",
        "dense_index.py",
        "sparse_index.py"
    ]
    
    for step in steps:
        run_step(step)
        
    print("\n=== Full Indexing Pipeline Completed ===")

if __name__ == "__main__":
    main()
