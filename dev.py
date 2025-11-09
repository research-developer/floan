#!/usr/bin/env python3
"""
Development Environment for svGen
Runs HTTP server + file watcher in parallel for live development.
"""
import os
import sys
import subprocess
import signal
import time
import threading
import select


def print_banner():
    """Print startup banner"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         🔷 svGen Development Environment                  ║
╚═══════════════════════════════════════════════════════════╝

Starting:
  1. HTTP Server on http://localhost:8000
  2. File Watcher for auto-regeneration

Workflow:
  1. Open http://localhost:8000/viewer.html in browser
  2. Edit Python files in examples/ or templates/
  3. Save file → Auto-regenerates → Refresh browser to see changes

Press Ctrl+C to stop all processes
""")


def stream_output(proc, label):
    """Stream output from a process in a separate thread"""
    try:
        for line in iter(proc.stdout.readline, ''):
            if line:
                sys.stdout.write(f"[{label}] {line}")
                sys.stdout.flush()
    except Exception as e:
        print(f"[{label}] Stream ended: {e}")


def main():
    """Run dev server and file watcher together"""

    print_banner()

    # Start both processes
    print("Starting HTTP Server...")
    server_proc = subprocess.Popen(
        [sys.executable, "dev_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    print("Starting File Watcher...")
    watcher_proc = subprocess.Popen(
        [sys.executable, "watch.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    processes = [
        (server_proc, "Server"),
        (watcher_proc, "Watcher")
    ]

    # Start threads to stream output
    threads = []
    for proc, label in processes:
        thread = threading.Thread(target=stream_output, args=(proc, label), daemon=True)
        thread.start()
        threads.append(thread)

    # Wait a moment for startup
    time.sleep(2)

    print("\n" + "="*60)
    print("✓ Development environment ready!")
    print("="*60)
    print("\n💡 Open http://localhost:8000/viewer.html\n")

    def cleanup(signum=None, frame=None):
        """Cleanup processes on exit"""
        print("\n\nShutting down...")
        for proc, name in processes:
            try:
                proc.terminate()
                proc.wait(timeout=3)
                print(f"✓ {name} stopped")
            except Exception:
                try:
                    proc.kill()
                    print(f"✓ {name} killed")
                except Exception:
                    pass
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        # Monitor processes
        while True:
            time.sleep(1)

            # Check if any process has died
            for proc, name in processes:
                if proc.poll() is not None:
                    print(f"\n✗ {name} exited with code {proc.returncode}")
                    cleanup()
                    return

    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
