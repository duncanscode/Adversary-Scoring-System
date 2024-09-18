from PIL import Image

KEY_POINTS = [
    (469, 1024),  # Center of the screen
    (1417, 450),  # Top-left corner
    (1403, 485),  # Top-right corner
    (503, 450),   # Bottom-left corner
]

def get_colors_from_image(image_path):
    # Open the image
    img = Image.open(image_path)

    # Get colors for each key point
    colors = []
    for x, y in KEY_POINTS:
        color = img.getpixel((x, y))
        colors.append(color)

    return colors

def main(image_path):
    colors = get_colors_from_image(image_path)
    
    print("Colors at key points:")
    for (x, y), color in zip(KEY_POINTS, colors):
        print(f"At point ({x}, {y}): RGB{color}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_image.png>")
    else:
        image_path = sys.argv[1]
        main(image_path)