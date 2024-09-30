from database import init_db, get_user_info, save_user_info
from versus_screen_analysis import detect_loading_screen
from replay_watcher import watch_replay_folder
from web_server import run_server
import time
import os
import threading

def get_user_input():
    username, replay_path = get_user_info()
    
    if not username:
        while True:
            username = input("Please enter your StarCraft II username: ").strip()
            if username:
                break
            print("Username cannot be empty. Please try again.")
    
    if not replay_path or not os.path.exists(replay_path):
        while True:
            replay_path = input("Please enter the full path to your StarCraft II replay folder: ").strip()
            if os.path.exists(replay_path):
                break
            print("Invalid path. Please make sure the folder exists.")
    
    save_user_info(username, replay_path)
    return username, replay_path

def main():
    # Initialize the database
    init_db()

    # Get or prompt for username and replay path
    username, replay_folder_path = get_user_input()
    
    print(f"Welcome, {username}!")
    print(f"Using replay folder: {replay_folder_path}")

    # Start the web server in a separate thread
    web_server_thread = threading.Thread(target=run_server)
    web_server_thread.start()

    print("Web server started. You can now add a Browser Source in OBS with the URL: http://localhost:5000")

    while True:
        if detect_loading_screen(username):
            print("Watching replay folder for new replays...")
            while True:
                new_replay_detected = watch_replay_folder(replay_folder_path, username)
                if new_replay_detected:
                    print("Restarting loading screen monitoring...")
                    break
                time.sleep(10)  # Check for new replays every 10 seconds
        time.sleep(0.5)  # Small delay before checking loading screen again

if __name__ == "__main__":
    main()