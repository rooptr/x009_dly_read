import urllib.request, json, re
from bs4 import BeautifulSoup

# Get file ID from WP-JSON
url = 'https://dailyepaper.in/wp-json/wp/v2/posts?slug=business-standard-epaper-feb-2026'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, timeout=15).read()
data = json.loads(response)
html = data[0]['content']['rendered']
soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a', href=True)
download_links = [(a['href'], a.text.strip()) for a in links if 'drive.google' in a['href'] and 'Download' in a.text]
match = re.search(r'/d/([a-zA-Z0-9_-]+)', download_links[0][0])
file_id = match.group(1)
print(f'File ID: {file_id}')

# Step 1: Hit the drive URL, get the virus scan page
direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
req1 = urllib.request.Request(direct_url, headers={'User-Agent': 'Mozilla/5.0'})
resp1 = urllib.request.urlopen(req1, timeout=30)
final_url = resp1.url
html1 = resp1.read().decode('utf-8', errors='ignore')

# Extract uuid
uuid_match = re.search(r'uuid"\\s*:\s*"([^"]+)"', html1)
uuid_val = uuid_match.group(1) if uuid_match else None
print(f'Redirected to: {final_url}')
print(f'UUID: {uuid_val}')

# Step 2: Construct the confirm URL on drive.usercontent.google.com
if uuid_val:
    confirm_url = f'https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t&uuid={uuid_val}'
    print(f'\n=== Trying confirm URL ===')
    print(f'URL: {confirm_url}')
    req2 = urllib.request.Request(confirm_url, headers={'User-Agent': 'Mozilla/5.0'})
    resp2 = urllib.request.urlopen(req2, timeout=60)
    content_type = resp2.headers.get('Content-Type', 'unknown')
    content_length = resp2.headers.get('Content-Length', 'unknown')
    first_bytes = resp2.read(20)
    print(f'Content-Type: {content_type}')
    print(f'Content-Length: {content_length}')
    print(f'Starts with PDF: {first_bytes[:4] == b"%PDF"}')
    print(f'First bytes: {first_bytes}')
else:
    print('No UUID found - cannot construct confirm URL')
