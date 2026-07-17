import http.server
import socketserver
import webbrowser

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# ponytail: simple server script, opens default browser tab automatically
print(f"Server started at http://localhost:{PORT}/viewer.html")
webbrowser.open(f"http://localhost:{PORT}/viewer.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
