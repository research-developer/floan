#!/usr/bin/env python3
"""
Simple Development Environment for svGen
Runs HTTP server + file watcher without output capture (most reliable).
"""
import os
import sys
import subprocess
import signal
import time


def main():
    """Run dev server and file watcher - simple version"""

    print("""
╔═══════════════════════════════════════════════════════════╗
║         🔷 svGen Development Environment (Simple)         ║
╚═══════════════════════════════════════════════════════════╝

Starting HTTP Server and File Watcher...
Their output will appear directly below.

💡 Open http://localhost:8000/viewer.html in your browser

Press Ctrl+C to stop all processes
""")

    # Start both processes - let them write to stdout directly
    server_proc = subprocess.Popen([sys.executable, "dev_server.py"])
    watcher_proc = subprocess.Popen([sys.executable, "watch.py"])

    processes = [server_proc, watcher_proc]

    def cleanup(signum=None, frame=None):
        """Cleanup processes on exit"""
        print("\n\nShutting down...")
        for proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        print("✓ Stopped")
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        # Just wait for processes
        while True:
            time.sleep(1)

            # Check if any process has died
            for proc in processes:
                if proc.poll() is not None:
                    print(f"\n✗ Process exited with code {proc.returncode}")
                    cleanup()
                    return

    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
