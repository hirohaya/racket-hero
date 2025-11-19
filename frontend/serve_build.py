#!/usr/bin/env python3
import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
BUILD_DIR = Path(__file__).parent / "build"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Se o arquivo não existe, servir index.html
        path = super().translate_path(path)
        if not os.path.exists(path):
            path = os.path.join(BUILD_DIR, "index.html")
        return path
    
    def end_headers(self):
        # Prevenir cache para development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

os.chdir(BUILD_DIR)

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()
