#!/usr/bin/env python3
"""
Development Server for svGen
Serves viewer.html with live reload capability.
"""
import http.server
import socketserver
import os
import sys

PORT = 8000
MAX_PORT = 8010  # Try up to port 8010


def main():
    """Start the development server"""

    # Change to repository root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)

    # Try to find an available port
    port = PORT
    httpd = None

    Handler = http.server.SimpleHTTPRequestHandler

    for port in range(PORT, MAX_PORT + 1):
        try:
            httpd = socketserver.TCPServer(("", port), Handler)
            httpd.allow_reuse_address = True
            break
        except OSError as e:
            if e.errno == 48:  # Address already in use (macOS)
                if port == MAX_PORT:
                    print(f"✗ Error: All ports {PORT}-{MAX_PORT} are in use!")
                    print(f"  Kill existing processes with: lsof -ti:{PORT} | xargs kill -9")
                    sys.exit(1)
                continue
            elif e.errno == 98:  # Address already in use (Linux)
                if port == MAX_PORT:
                    print(f"✗ Error: All ports {PORT}-{MAX_PORT} are in use!")
                    print(f"  Kill existing processes with: lsof -ti:{PORT} | xargs kill -9")
                    sys.exit(1)
                continue
            else:
                raise

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║         🔷 svGen Development Server                       ║
╚═══════════════════════════════════════════════════════════╝

Server running at: http://localhost:{port}
Viewer URL:        http://localhost:{port}/viewer.html

Instructions:
1. Open http://localhost:{port}/viewer.html in your browser
2. Edit your Python scripts (examples/, templates/)
3. Run the script to generate new SVGs
4. Refresh the browser to see results

Press Ctrl+C to stop the server
""")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    finally:
        if httpd:
            httpd.shutdown()
            httpd.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()
