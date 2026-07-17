import urllib.request, json, re, http.cookiejar, urllib.parse
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

# Use cookie jar to handle cookies across redirects
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Step 1: Initial request
direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
req1 = urllib.request.Request(direct_url, headers={'User-Agent': 'Mozilla/5.0'})
resp1 = opener.open(req1, timeout=30)
html1 = resp1.read().decode('utf-8', errors='ignore')
print(f'\nStep 1 - URL: {resp1.url}')
print(f'Step 1 - Cookies: {[c.name for c in cj]}')

# Hidden form fields
form_inputs = re.findall(r'<input[^>]*name="(\w+)"[^>]*value="([^"]*)"', html1)
print(f'\nHidden form fields:')
for name, value in form_inputs:
    print(f'  {name} = {value[:80] if len(value) > 80 else value}')

# POST request
print('\n=== Trying POST with form data ===')
form_data = {name: value for name, value in form_inputs if value}
form_data['export'] = 'download'
form_data['id'] = file_id
encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
req2 = urllib.request.Request(direct_url, data=encoded_data, headers={
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded'
})
try:
    resp2 = opener.open(req2, timeout=30)
    content_type = resp2.headers.get('Content-Type', 'unknown')
    content_length = resp2.headers.get('Content-Length', 'unknown')
    first_bytes = resp2.read(20)
    print(f'Content-Type: {content_type}')
    print(f'Content-Length: {content_length}')
    print(f'Starts with PDF: {first_bytes[:4] == b"%PDF"}')
    print(f'First bytes: {first_bytes}')
except Exception as e:
    print(f'POST error: {e}')
