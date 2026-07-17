import urllib.request
import re

url = 'https://www.careerswave.in/the-financial-express-epaper-pdf-free-download/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    
    # regex search for DD-MM-YYYY followed closely by a drive link
    matches = re.findall(r'(\d{2}-\d{2}-\d{4}).*?(https://drive\.google\.com/[^\s"\'<>]+)', html, re.DOTALL)
    print("Found Date-Link Mappings:")
    for m in matches[:5]:
        print(f"Date: {m[0]} -> Link: {m[1]}")
        
except Exception as e:
    print(e)
