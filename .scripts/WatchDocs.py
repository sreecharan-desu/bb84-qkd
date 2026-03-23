import sys
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Paths
WATCH_DIR = "docs"
MAKE_CMD  = ["make", "all"]

class LaTeXWatcher(FileSystemEventHandler):
    \"\"\"Watches for changes in LaTeX source files.\"\"\"

    def __init__(self):
        self.last_run = 0
        self.cooldown = 2  # Wait 2 seconds before rebuilding again

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only watch .tex and .bib files
        if event.src_path.endswith(('.tex', '.bib', '.md')):
            now = time.time()
            if now - self.last_run > self.cooldown:
                print(f"\\nDocument change detected: {event.src_path}")
                print("Rebuilding PDF...")
                try:
                    subprocess.run(MAKE_CMD, check=True)
                    self.last_run = now
                except Exception as e:
                    print(f"Error rebuilding paper: {e}")

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        print(f"Error: {WATCH_DIR} directory not found.")
        sys.exit(1)

    print(f"Starting document watcher on {WATCH_DIR}/...")
    print("PDF will rebuild automatically in the root folder when you edit LaTeX or Markdown sources.")
    print("Press Ctrl+C to stop.")

    event_handler = LaTeXWatcher()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
