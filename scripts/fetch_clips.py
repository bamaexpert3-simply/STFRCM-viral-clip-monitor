import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_data(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read()
    except Exception as e:
        print(f"Skipping source due to timeout or block: {url}")
        return None

def main():
    print("Initializing STFRCM Data Ingestion...")
    
    feed_map = {
        "CNN": "http://cnn.com",
        "ABC": "https://go.com"
    }
    
    master_clips = []
    
    for category, url in feed_map.items():
        raw_xml = fetch_data(url)
        if not raw_xml:
            continue
        try:
            root = ET.fromstring(raw_xml)
            for item in root.findall('.//item')[:15]:
                title = item.find('title').text if item.find('title') is not None else "Viral Clip"
                link = item.find('link').text if item.find('link') is not None else "#"
                
                master_clips.append({
                    "title": title,
                    "url": link,
                    "category": category,
                    "score": 95,
                    "timestamp": datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            print(f"Parsing skip: {e}")
            
    output_payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_clips": len(master_clips),
        "trends": [{"topic": "Short Form Video Growth", "volume": "500K+"}],
        "clips": master_clips
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/clips.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully tracked {len(master_clips)} media elements.")

if __name__ == "__main__":
    main()
