from database import init_db
from versus_screen_analysis import detect_loading_screen
from replay_watcher import watch_replay_folder
import time

def main():
    # Initialize the database
    init_db()

    replay_folder_path = "C:/Users/Pablo/Documents/StarCraft II/Accounts/50459048/1-S2-1-3384607/Replays/Multiplayer"

    while True:
        if detect_loading_screen():
            print("Watching replay folder for new replays...")
            while True:
                new_replay_detected = watch_replay_folder(replay_folder_path)
                if new_replay_detected:
                    print("New replay detected and analyzed. Restarting loading screen monitoring...")
                    break
                time.sleep(10)  # Check for new replays every 10 seconds
        time.sleep(0.5)  # Small delay before checking loading screen again

if __name__ == "__main__":
    main()