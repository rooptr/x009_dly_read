import urllib.request
import json
from bs4 import BeautifulSoup
import re

url = 'https://www.careerswave.in/wp-json/wp/v2/posts?slug=the-financial-express-epaper-pdf-free-download'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req).read()
data = json.loads(res)

if data:
    html = data[0]['content']['rendered']
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if 'drive' in a['href'] or 'pdf' in a['href'].lower() or 'telegram' in a['href']:
            print("Found link:", a['href'], "Text:", a.text)
else:
    print("No data found")
