#!/usr/bin/env python3
"""
File Watcher for svGen
Automatically regenerates SVGs when Python files are modified.
"""
import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

WATCH_DIRS = ['examples', 'templates', 'src']
WATCH_EXTENSIONS = ['.py']
CHECK_INTERVAL = 1.0  # seconds


def get_file_mtime(filepath):
    """Get modification time of a file"""
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return None


def get_all_watched_files():
    """Get all Python files in watched directories"""
    files = {}
    for directory in WATCH_DIRS:
        dir_path = Path(directory)
        if dir_path.exists():
            for ext in WATCH_EXTENSIONS:
                for filepath in dir_path.rglob(f'*{ext}'):
                    files[str(filepath)] = get_file_mtime(filepath)
    return files


def run_script(filepath):
    """Run a Python script and return success status"""
    print(f"\n{'='*60}")
    print(f"🔄 Running: {filepath}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"✓ Success at {timestamp}")
            return True
        else:
            print(f"✗ Failed with exit code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ Script timed out (30s limit)")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Watch for file changes and auto-regenerate"""

    print("""
╔═══════════════════════════════════════════════════════════╗
║         🔷 svGen File Watcher                             ║
╚═══════════════════════════════════════════════════════════╝

Watching for changes in:
  - examples/
  - templates/
  - src/

When a file changes, it will automatically run and regenerate SVGs.
Press Ctrl+C to stop watching
""")

    # Initial file states
    file_states = get_all_watched_files()
    print(f"Watching {len(file_states)} files...\n")

    try:
        while True:
            time.sleep(CHECK_INTERVAL)

            # Check for changes
            current_states = get_all_watched_files()

            # Find changed or new files
            for filepath, mtime in current_states.items():
                if filepath not in file_states or file_states[filepath] != mtime:
                    # File was modified or created
                    file_states[filepath] = mtime

                    # Only auto-run example and template files, not src
                    if filepath.startswith('examples/') or filepath.startswith('templates/'):
                        run_script(filepath)

            # Remove deleted files from tracking
            deleted_files = set(file_states.keys()) - set(current_states.keys())
            for filepath in deleted_files:
                print(f"📁 File deleted: {filepath}")
                del file_states[filepath]

    except KeyboardInterrupt:
        print("\n\n✓ Watcher stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()
