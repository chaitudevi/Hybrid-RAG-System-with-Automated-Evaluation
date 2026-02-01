import json
import requests
import time
from tqdm import tqdm

def fetch_fixed_urls(n=200):
    collected_urls = []
    
    print(f"Fetching {n} random URLs for Fixed Set from Wikipedia...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    pbar = tqdm(total=n)
    
    while len(collected_urls) < n:
        try:
            # Special:Random redirects to a random article
            r = requests.get("https://en.wikipedia.org/wiki/Special:Random", headers=headers, timeout=10)
            url = r.url
            
            if url not in collected_urls:
                collected_urls.append(url)
                pbar.update(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            
    pbar.close()
    return collected_urls

if __name__ == "__main__":
    urls = fetch_fixed_urls(200)
    with open("data/fixed_urls.json", "w") as f:
        json.dump(urls, f, indent=2)
    print(f"Saved {len(urls)} URLs to data/fixed_urls.json")
