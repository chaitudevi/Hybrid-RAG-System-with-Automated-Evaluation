import requests
import json

url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
try:
    print(f"Fetching {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.text)}")
    print("Preview:")
    print(response.text[:200])
except Exception as e:
    print(f"Error: {e}")
