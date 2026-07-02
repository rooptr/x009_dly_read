import urllib.request
from bs4 import BeautifulSoup
import re
import os
import json

papers = {
    "et.pdf": "https://dailyepaper.in/economic-times-newspaper-today-2026/",
    "bs.pdf": "https://dailyepaper.in/business-standard-epaper-feb-2026/",
    "fe.pdf": "https://dailyepaper.in/financial-express-newspaper-free-download-2026/",
    "mint.pdf": "https://dailyepaper.in/live-mint-epaper-feb-2026/"
}

def fetch_paper(filename, url):
    print(f"\nFetching {filename} from {url} ...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        links = soup.find_all('a', href=True)
        drive_link = None
        for a in links:
            if 'drive.google' in a['href'] and 'Download' in a.text:
                drive_link = a['href']
                break
                
        if drive_link:
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_link)
            if match:
                file_id = match.group(1)
                direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                print(f"Downloading {filename}...")
                urllib.request.urlretrieve(direct_url, filename)
                size = os.path.getsize(filename)
                print(f"Success! Downloaded {filename} ({size / 1024 / 1024:.2f} MB)")
            else:
                print(f"Could not extract file ID for {filename}.")
        else:
            print(f"No drive link found for {filename}.")
    except Exception as e:
        print(f"Error fetching {filename}: {e}")

def fetch_gold_rate():
    print("\nFetching 24K Gold Rate from goodreturns.in ...")
    url = "https://www.goodreturns.in/gold-rates/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        tables = soup.find_all('table')
        for t in tables:
            if '24K' in t.text and 'Gram' in t.text:
                tds = t.find_all('td')
                for td in tds:
                    if '₹' in td.text:
                        price = td.text.strip().replace(',', '')
                        match = re.search(r'₹\s*(\d+)', price)
                        if match:
                            rate = f"₹{int(match.group(1)):,}"
                            with open('gold_rate.json', 'w', encoding='utf-8') as f:
                                json.dump({'rate': rate}, f)
                            print(f"Success! Gold Rate is {rate}")
                            return
        print("Could not find the gold rate in the tables.")
    except Exception as e:
        print(f"Error fetching gold rate: {e}")

if __name__ == "__main__":
    for filename, url in papers.items():
        fetch_paper(filename, url)
    fetch_gold_rate()
