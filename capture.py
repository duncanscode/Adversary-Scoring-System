import cv2
import mss
import numpy as np

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Use the primary monitor
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR for OpenCV
    return img

def capture_region(image, region):
    x, y, w, h = region
    return image[y:y+h, x:x+w]
