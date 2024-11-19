<<<<<<< HEAD
import os
import random
import json
from PIL import Image
from dif import image_color_difference  # Assuming dif.py is in the same directory

def place_object_and_score(background_path, object_folder, output_folder, filled_image_path, max_attempts=100):  # Added max_attempts
    """
    Places objects from a folder onto a background image at random positions, sizes, rotations, and tints,
    calculates the score, and saves the results. Also saves the highest score in a JSON file.
    Stops after a specified number of attempts.

    Args:
        background_path (str): Path to the background image (image.jpg).
        object_folder (str): Path to the folder containing object images.
        output_folder (str): Path to the folder where results will be saved.
        filled_image_path (str): Path to the filled image (filled.jpg).
        max_attempts (int): Maximum number of attempts to run.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    background = Image.open(background_path).convert("RGBA")  # Ensure background is in RGBA mode
    object_files = [f for f in os.listdir(object_folder) if f.endswith('.png')]  # Assuming .png format

    best_attempt = None
    best_score = float('-inf')

    for attempt_number in range(max_attempts):  # Iterate up to max_attempts
        # Pick a random object file
        object_file = random.choice(object_files)
        object_path = os.path.join(object_folder, object_file)
        object_image = Image.open(object_path).convert("RGBA")  # Ensure object is in RGBA mode

        # Place object at a random position, size, rotation, and tint
        modified_background = place_object_random(background, object_image)
        
        # Save the modified background
        modified_background_path = os.path.join(output_folder, f"temp_modified.png")
        modified_background.save(modified_background_path)

        # Calculate score using image_color_difference
        score = image_color_difference(modified_background_path, filled_image_path)

        # Create directory for this attempt
        attempt_output_dir = os.path.join(output_folder, f"{attempt_number + 1}_{score}")
        if not os.path.exists(attempt_output_dir):
            os.makedirs(attempt_output_dir)

        # Move and rename the modified background
        final_modified_path = os.path.join(attempt_output_dir, f"modified_{attempt_number + 1}.png")
        os.rename(modified_background_path, final_modified_path)

        # Move the difference colormap (assuming it's saved as 'difference_colormap.png' by your function)
        os.rename("difference_colormap.png", os.path.join(attempt_output_dir, "difference_colormap.png"))

        print(f"Attempt {attempt_number + 1}: Score = {score}, saved in {attempt_output_dir}")

        if score > best_score:
            best_score = score
            best_attempt = f"{attempt_number + 1}_{score}"

    # Save the best attempt in a JSON file
    if best_attempt:
        with open(os.path.join(output_folder, "highest_score.json"), "w") as f:
            json.dump({"highest_score": best_attempt}, f)
        print(f"Highest score: {best_attempt}, saved in highest_score.json")

def place_object_random(background, object_image):
    """Places the object image at a random position, size, rotation, and tint on the background image."""
    bg_w, bg_h = background.size
    obj_w, obj_h = object_image.size

    # Generate random scale factor between 0.25 and 4.0
    scale_factor = random.uniform(0.25, 4.0)
    new_obj_w = int(obj_w * scale_factor)
    new_obj_h = int(obj_h * scale_factor)
    resized_object = object_image.resize((new_obj_w, new_obj_h), Image.LANCZOS)

    # Generate random rotation angle
    angle = random.uniform(0, 360)
    rotated_object = resized_object.rotate(angle, expand=True)

    # Generate random tint color
    tint_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tinted_object = apply_tint(rotated_object, tint_color)

    # Generate random position (allowing objects to be slightly off the edge)
    rot_w, rot_h = tinted_object.size
    x = random.randint(-rot_w // 2, bg_w - rot_w // 2)
    y = random.randint(-rot_h // 2, bg_h - rot_h // 2)

    # Create a new image with the same size as the background and paste the background onto it
    temp_background = Image.new("RGBA", background.size)
    temp_background.paste(background, (0, 0))

    # Paste the tinted object at the random position
    temp_background.paste(tinted_object, (x, y), tinted_object)

    return temp_background

def apply_tint(image, tint_color):
    """Applies a tint color to the image while preserving transparency and gradients."""
    tinted_image = Image.new("RGBA", image.size)
    pixels = image.load()
    tinted_pixels = tinted_image.load()

    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            tr, tg, tb = tint_color

            # Blend the tint color with the original color based on the alpha channel
            if a == 0:
                tinted_pixels[i, j] = (0, 0, 0, 0)  # Preserve full transparency
            else:
                alpha = a / 255.0
                new_r = int((1 - alpha) * r + alpha * tr)
                new_g = int((1 - alpha) * g + alpha * tg)
                new_b = int((1 - alpha) * b + alpha * tb)
                tinted_pixels[i, j] = (new_r, new_g, new_b, a)

    return tinted_image

# Example Usage (adjust paths as needed)
place_object_and_score("image.jpg", "object", "output", "filled.jpg", max_attempts=500)
=======
import cv2
import numpy as np

def calculate_color_difference(image1_path, image2_path):
    # Read images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    if img1 is None or img2 is None:
        raise ValueError("One or both images not found")

    # Ensure images are of the same size
    if img1.shape != img2.shape:
        raise ValueError("Images must be of the same size")

    # Calculate absolute difference
    diff = cv2.absdiff(img1, img2)

    # Convert difference to grayscale for simplicity
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Save grayscale difference for debugging
    cv2.imwrite('grayscale_difference.png', gray_diff)

    # Define color mapping thresholds and colors
    thresholds = [0, 50, 100, 150]
    colors = [
        (0, 0, 255),       # Red
        (0, 165, 255),     # Orange
        (0, 255, 0),       # Green
        (173, 216, 230)    # Light Blue
    ]

    # Create an empty image to hold the color map
    color_map = np.zeros_like(img1)

    # Map grayscale differences to colors
    for i in range(len(thresholds) - 1):
        mask = (gray_diff >= thresholds[i]) & (gray_diff < thresholds[i + 1])
        color_map[mask] = colors[i]

    # For values equal to or greater than the last threshold
    mask = (gray_diff >= thresholds[-1])
    color_map[mask] = colors[-1]

    # Save color map for debugging
    cv2.imwrite('color_map_debug.png', color_map)

    # Calculate a score based on the average difference
    avg_diff = np.mean(gray_diff)
    score = int(avg_diff)

    # Save the color map with the score as the filename
    output_filename = f"color_map_score_{score}.png"
    cv2.imwrite(output_filename, color_map)

    return output_filename, score

# Example usage
image1_path = 'image.jpg'
image2_path = 'filled.jpg'
output_filename, score = calculate_color_difference(image1_path, image2_path)
print(f"Color map saved as {output_filename} with score {score}")
>>>>>>> 925187bca08e7c708e36339e9d2d8afa436e5267
