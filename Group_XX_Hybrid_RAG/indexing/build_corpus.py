import os
import json
import requests
from bs4 import BeautifulSoup
import yaml
from tqdm import tqdm

def load_config():
    with open("../config.yaml", "r") as f:
        return yaml.safe_load(f)

def fetch_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def clean_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # target main content for Wikipedia
    content = soup.find(id="mw-content-text")
    if content:
        soup = content
        
    # Remove unwanted elements
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "table"]):
        element.extract()
        
    # Remove specific classes for Wikipedia noise
    for element in soup.find_all(class_=["mw-editsection", "reference", "reflist", "mw-empty-elt", "noprint"]):
        element.extract()
        
    text = soup.get_text(separator=" ")
    
    # Clean whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text

def fetch_random_urls(n=300):
    random_endpoint = "https://en.wikipedia.org/wiki/Special:Random"
    collected_urls = []
    attempts = 0
    max_attempts = n * 5 # Avoid infinite loops
    
    print(f"Fetching {n} random URLs (min 200 words)...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    pbar = tqdm(total=n)
    
    while len(collected_urls) < n and attempts < max_attempts:
        try:
            # Requests follows redirects by default, so hitting Special:Random gives us a real article
            response = requests.get(random_endpoint, headers=headers, timeout=10)
            final_url = response.url
            
            # Skip if we already have this URL
            if final_url in collected_urls:
                attempts += 1
                continue
                
            text = clean_text(response.text)
            word_count = len(text.split())
            
            if word_count >= 200:
                collected_urls.append(final_url)
                pbar.update(1)
            else:
                pass # Skip short articles
                
        except Exception as e:
            print(f"Error fetching random: {e}")
            
        attempts += 1
        
    pbar.close()
    
    # Save the random URLs for reproducibility of this run
    with open("../data/random_urls.json", "w") as f:
        json.dump(collected_urls, f, indent=2)
        
    return collected_urls

def build_corpus():
    config = load_config()
    
    # 1. Process Fixed URLs
    fixed_urls_path = "../data/fixed_urls.json"
    fixed_documents = []
    
    if os.path.exists(fixed_urls_path):
        with open(fixed_urls_path, "r") as f:
            fixed_urls = json.load(f)
            
        print("Fetching Fixed URLs...")
        for i, url in enumerate(tqdm(fixed_urls)):
            html = fetch_url(url)
            if html:
                text = clean_text(html)
                # fixed URLs are curated to be >200 words, 
                
                
                doc_id = f"doc_fixed_{i:03d}"
                fixed_documents.append({
                    "id": doc_id,
                    "url": url,
                    "text": text,
                    "source": "fixed"
                })
    
    # 2. Process Random URLs
    random_urls = fetch_random_urls(n=300)
    random_documents = []
    
    print("Processing Random URLs content...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for i, url in enumerate(tqdm(random_urls)):
        # We already fetched them in fetch_random_urls to validate count, 
        # but to keep logic clean we'll re-fetch or (better) refactor to save text during validation? 
        # For simplicity/robustness, let's re-fetch OR refactor fetch_random to return data.
        # Let's refactor fetch_random slightly to return the data so we don't double hit.
        pass

    # Actually, let's Optimize: fetch_random_urls should return the data/text to avoid double scraping
    # Redefining fetch_random_urls strategy below in the actual code execution
    pass
    
    # ... (Wait, I cannot redefine inside the string. I will rewrite the function logic in the ReplacementContent correctly)
    
    pass 

# Let's try again with the correct complete logic block
def fetch_and_process_random(n=300):
    random_endpoint = "https://en.wikipedia.org/wiki/Special:Random"
    documents = []
    attempts = 0
    max_attempts = n * 5 
    
    print(f"Fetching {n} random URLs (min 200 words)...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    collected_urls = []
    pbar = tqdm(total=n)
    
    while len(documents) < n and attempts < max_attempts:
        try:
            response = requests.get(random_endpoint, headers=headers, timeout=10)
            final_url = response.url
            
            if final_url in collected_urls:
                attempts += 1
                continue
            
            text = clean_text(response.text)
            if len(text.split()) >= 200:
                doc_id = f"doc_random_{len(documents):03d}"
                documents.append({
                    "id": doc_id,
                    "url": final_url,
                    "text": text,
                    "source": "random"
                })
                collected_urls.append(final_url)
                pbar.update(1)
        except Exception:
            pass
        attempts += 1
    pbar.close()
    
    with open("../data/random_urls.json", "w") as f:
        json.dump(collected_urls, f, indent=2)
        
    return documents

def build_corpus():
    config = load_config()
    
    # 1. Fixed
    fixed_docs = []
    fixed_path = "../data/fixed_urls.json"
    if os.path.exists(fixed_path):
        with open(fixed_path, "r") as f:
            urls = json.load(f)
        print("Fetching Fixed URLs...")
        for i, url in enumerate(tqdm(urls)):
            html = fetch_url(url)
            if html:
                text = clean_text(html)
                if len(text.split()) >= 200: # Enforce here too for safety
                    fixed_docs.append({
                        "id": f"doc_fixed_{i:03d}",
                        "url": url,
                        "text": text,
                        "source": "fixed"
                    })
    
    # 2. Random
    random_docs = fetch_and_process_random(n=300)
    
    all_docs = fixed_docs + random_docs
    
    os.makedirs("../data/processed", exist_ok=True)
    with open("../data/processed/documents.jsonl", "w", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc) + "\n")
            
    print(f"Saved {len(all_docs)} documents ({len(fixed_docs)} fixed, {len(random_docs)} random) to ../data/processed/documents.jsonl")

if __name__ == "__main__":
    build_corpus()
