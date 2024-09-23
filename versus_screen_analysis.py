from thefuzz import fuzz, process
import cv2
import pytesseract
import re
import numpy as np
import time
import mss
import mss.tools
from difflib import get_close_matches
from capture import capture_screen, capture_region
from database import save_to_db, fetch_data
import keyboard

# Define the key points to check and their expected colors
# Format: (x, y, (r, g, b))
KEY_POINTS = [
    (469, 1024, (254, 196, 40)),  # Center of the screen, dark blue
    (1417, 450, (61, 44, 40)),  # Top-left corner, white
    (1403, 485, (45, 32, 30)),  # Top-right corner, dark blue
    (503, 450, (61, 44, 40)),  # Bottom-left corner, dark blue
]

# Define the regions of interest for the usernames and map name
user_name_region = (245, 439, 200, 27)  # (x, y, width, height) for your username
opponent_name_region = (1470, 440, 200, 27)  # (x, y, width, height) for opponent's username
map_name_region = (750, 693, 430, 60)  # (x, y, width, height) for map name
full_screen_region = (0, 0, 1920, 1080)

current_map_pool = [
    "Alcyone LE",
    "Amphion LE",
    "Crimson Court LE",
    "Dynasty LE",
    "Ghost River LE",
    "Goldenaura LE",
    "Oceanborn LE",
    "Post-Youth LE",
    "Site Delta LE"
]

def check_loading_screen():

    with mss.mss() as sct:
        img = np.array(sct.grab(sct.monitors[1]))
    matching_points = 0
    for x, y, expected_color in KEY_POINTS:
        actual_color = img[y, x][:3]  # Note: y comes before x in numpy arrays
        if np.array_equal(actual_color, expected_color):
            matching_points += 1
        
    
    result = matching_points == len(KEY_POINTS)

    return result  # All points must match exactly

def detect_loading_screen(username):
    print("Detecting loading screen")
    consecutive_detections = 0
    
    while True:
        if check_loading_screen():
            consecutive_detections += 1
            if consecutive_detections >= 3:  # Require 3 consecutive detections
                print("Loading screen detected!")
                scrape_details(username)
                return True
        else:
            consecutive_detections = 0
        
        time.sleep(0.1)  # Check every 0.1 seconds

def extract_text_from_region(image, region, region_name):
    # Crop the region of interest
    cropped_image = capture_region(image, region)
    
    # Generate a unique filename using the current timestamp
    timestamp = int(time.time() * 1000)
    filename = f'{region_name}_{timestamp}.png'
    
    # Preprocess the image
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    
    # Apply OCR with a custom config
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789<>'
    text = pytesseract.image_to_string(gray_image, config=custom_config).strip()

    # Save the cropped image for debugging if required
    # DEBUGGING ONLY
    # cv2.imwrite(filename, cropped_image)
    
    # Post-process the text (e.g., remove non-alphanumeric characters)
    cleaned_text = re.sub(r'[^A-Za-z0-9<>]', '', text)

    clan_removed = re.sub(r'^.*?>', '', text)
    
    return clan_removed

def fuzzy_match_map_name(extracted_map_name, current_map_pool):
    # DEBUGGING
    # print(f"Original extracted map name: '{extracted_map_name}'")
    
    if not extracted_map_name:
        print("Extracted map name is empty")
        return None
    
    # Remove any non-alphanumeric characters and convert to lowercase
    cleaned_map_name = ''.join(char.lower() for char in extracted_map_name if char.isalnum() or char.isspace()).strip()
    
    # DEBUGGING
    # print(f"Cleaned map name: '{cleaned_map_name}'")
    
    if not cleaned_map_name:
        print("Cleaned map name is empty")
        return None 
    
    # Perform fuzzy matching
    best_match, score = process.extractOne(cleaned_map_name, current_map_pool)
    
    print(f"Best match: '{best_match}' with score: {score}")
    
    # You might want to adjust this threshold
    if score > 60:
        return best_match
    else:
        print(f"No good match found. Best score was {score}")
        return None

def scrape_details(username):
    image = capture_screen()
    # Extract text from defined regions
    full_screen = extract_text_from_region(image, full_screen_region, "full-screen")
    user_name = extract_text_from_region(image, user_name_region, "user_name_region")
    opponent_name = extract_text_from_region(image, opponent_name_region, "opponent_name_region")
    map_name = extract_text_from_region(image, map_name_region, "map_name_region")
    
    # print(f"Extracted user name: '{user_name}'")
    # print(f"Extracted opponent name: '{opponent_name}'")
    # print(f"Extracted map name: '{map_name}'")
    
    # Attempt to fuzzy match the map name
    matched_map_name = fuzzy_match_map_name(map_name, current_map_pool)
    if matched_map_name:
        # Remove "Team 1" and "Team 2" and any invalid characters
        player1 = user_name
        player2 = opponent_name
        
        # DEBUGGING
        # print(f"Player1: '{player1}'")
        # print(f"Player2: '{player2}'")
        
        if player1.lower() != username.lower():
            opponent_name = player1
        else:
            opponent_name = player2
        
        print(f"Opponent Name: {opponent_name}")
        print(f"Map Name: {matched_map_name}")
        calculate_win_loss(opponent_name)
    else:
        print(f"No valid 1v1 data could be identified. Map name parsed as: '{map_name}'")

def calculate_win_loss(oppname):
    query = "SELECT SUM(wins) AS total_wins, SUM(losses) AS total_losses FROM matches WHERE opponent_name = ?;"
    results = fetch_data(query, (oppname,))
    
    if results and len(results) > 0:
        total_wins, total_losses = results[0]
        total_wins = total_wins or 0  # Convert None to 0
        total_losses = total_losses or 0  # Convert None to 0
        print(f"Total wins against {oppname}: {total_wins}")
        print(f"Total losses against {oppname}: {total_losses}")
    else:
        print(f"No data found for opponent: {oppname}")
        total_wins, total_losses = 0, 0
    
    return total_wins, total_losses

def main_detect_loading_screen(username):
    if detect_loading_screen(username):
        print("Loading screen detected and details scraped.")
        return True
    return False