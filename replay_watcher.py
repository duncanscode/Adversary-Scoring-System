import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from parse_replay import replay_parser
import os

class ReplayHandler(FileSystemEventHandler):
    def __init__(self, username):
        self.new_replay_detected = False
        self.username = username

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            _, file_extension = os.path.splitext(file_path)
            
            if file_extension.lower() == '.sc2replay':
                print(f"New replay file detected: {file_path}")
                time.sleep(5)  # Wait for the file to be fully written
                if os.path.exists(file_path):  # Check if the file still exists
                    replay_parser(file_path, self.username)
                    self.new_replay_detected = True
                else:
                    print(f"File no longer exists: {file_path}")
            else:
                print(f"Ignored file: {file_path}")

def watch_replay_folder(folder_path, username):
    print("Watching replay folder")
    event_handler = ReplayHandler(username)
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()
    
    try:
        while True:
            if event_handler.new_replay_detected:
                print("New replay detected and analyzed.")
                break
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
    
    return event_handler.new_replay_detected