#!/usr/bin/env python3
"""Ultra-simple test server"""
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting server on port {PORT}...")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()
