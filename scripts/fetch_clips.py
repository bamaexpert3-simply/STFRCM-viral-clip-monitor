import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_data(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read()
    except Exception as e:
        print(f"Error pulling from source: {e}")
        return None

def parse_rss_feed(xml_data, category_name):
    clips = []
    if not xml_data:
        return clips
    try:
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')
        if not items:
            items = root.findall('.//{http://w3.org}entry')
            
        for item in items[:20]:
            title_node = item.find('title') or item.find('{http://w3.org}title')
            link_node = item.find('link') or item.find('{http://w3.org}link')
            title = title_node.text if title_node is not None else "Viral Clip"
            
            if link_node is not None:
                link = link_node.text if link_node.text else link_node.get('href', '#')
            else:
                link = '#'
                
            clips.append({
                "title": title,
                "url": link,
                "category": category_name,
                "score": 90,
                "timestamp": datetime.now().strftime("%Y-%m-%d")
            })
    except Exception as e:
        print(f"Parsing error for {category_name}: {e}")
    return clips

def main():
    print("Initializing complete STFRCM Data Ingestion Array...")
    
    feed_map = {
        "NFL": "https://youtube.com",
        "NBA": "https://youtube.com",
        "WNBA": "https://youtube.com",
        "MLB": "https://youtube.com",
        "NHL": "https://youtube.com",
        "NCAA": "https://youtube.com",
        "CNN": "http://cnn.com",
        "MSNBC": "https://youtube.com",
        "ABC": "https://go.com",
        "White House": "https://youtube.com",
        "TMZ": "https://youtube.com",
        "Funny Clips": "https://reddit.com",
        "Furry Animals": "https://reddit.com"
    }
    
    master_clips = []
    for category, url in feed_map.items():
        print(f"Scraping category segment: {category}")
        raw_xml = fetch_data(url)
        category_clips = parse_rss_feed(raw_xml, category)
        master_clips.extend(category_clips)
        
    print("Ingesting current Google Trends matrix...")
    trends_url = "https://google.com"
    trends_xml = fetch_data(trends_url)
    trends_list = []
    
    if trends_xml:
        try:
            root = ET.fromstring(trends_xml)
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text if item.find('title') is not None else ""
                traffic = item.find('{https://google.com}approx_traffic')
                traffic_text = traffic.text if traffic is not None else "100K+"
                if title:
                    trends_list.append({"topic": title, "volume": traffic_text})
        except Exception:
            pass

    output_payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_clips": len(master_clips),
        "trends": trends_list,
        "clips": master_clips
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/clips.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)
        
    print(f"Sync complete. Compiled {len(master_clips)} dynamic assets into database.")

if __name__ == "__main__":
    main()
