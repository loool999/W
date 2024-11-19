import os
import random
import json
from PIL import Image
from dif import image_color_difference 

background_path="filled.jpg"
object_folder="object"
output_folder="output"
filled_image_path="image.jpg"
size_min=0.25
size_max=4
max_attempts=100


def place_object_and_score(background_path=background_path, object_folder=object_folder, output_folder=output_folder, filled_image_path=filled_image_path, max_attempts=max_attempts):  # Added max_attempts
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
    object_files = [f for f in os.listdir(object_folder) if f.endswith('.png')] 

    best_attempt = None
    best_score = float('-inf')

    for attempt_number in range(max_attempts):  # max_attempts
        # Pick a random object file
        object_file = random.choice(object_files)
        object_path = os.path.join(object_folder, object_file)
        object_image = Image.open(object_path).convert("RGBA")  # Ensure object is in RGBA mode

        # Random thingy
        modified_background = place_object_random(background, object_image)
        
        # Save
        modified_background_path = os.path.join(output_folder, f"temp_modified.png")
        modified_background.save(modified_background_path)

        # Calculate score
        score = image_color_difference(modified_background_path, filled_image_path)

        # Create directory
        attempt_output_dir = os.path.join(output_folder, f"{attempt_number + 1}_{score}")
        if not os.path.exists(attempt_output_dir):
            os.makedirs(attempt_output_dir)

        # Move and rename
        final_modified_path = os.path.join(attempt_output_dir, f"modified_{attempt_number + 1}.png")
        os.rename(modified_background_path, final_modified_path)

        # Move the colormap 
        os.rename("difference_colormap.png", os.path.join(attempt_output_dir, "difference_colormap.png"))

        print(f"Attempt {attempt_number + 1}: Score = {score}, saved in {attempt_output_dir}")

        if score > best_score:
            best_score = score
            best_attempt = f"{attempt_number + 1}_{score}"

    # Save the best attempt
    if best_attempt:
        with open(os.path.join(output_folder, "highest_score.json"), "w") as f:
            json.dump({"highest_score": best_attempt}, f)
        print(f"Highest score: {best_attempt}, saved in highest_score.json")

def place_object_random(background, object_image):
    """Places the object image at a random position, size, rotation, and tint on the background image."""
    bg_w, bg_h = background.size
    obj_w, obj_h = object_image.size

    # Generate random scale
    scale_factor = random.uniform(size_min, size_max)
    new_obj_w = int(obj_w * scale_factor)
    new_obj_h = int(obj_h * scale_factor)
    resized_object = object_image.resize((new_obj_w, new_obj_h), Image.LANCZOS)

    # Generate random rotation angle
    angle = random.uniform(0, 360)
    rotated_object = resized_object.rotate(angle, expand=True)

    # Generate random tint color
    tint_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tinted_object = apply_tint(rotated_object, tint_color)

    # Generate random position
    rot_w, rot_h = tinted_object.size
    x = random.randint(-rot_w // 2, bg_w - rot_w // 2)
    y = random.randint(-rot_h // 2, bg_h - rot_h // 2)

    # Create a new image with the same size as the background and paste the background onto it
    temp_background = Image.new("RGBA", background.size)
    temp_background.paste(background, (0, 0))

    # Paste the object at a random position
    temp_background.paste(tinted_object, (x, y), tinted_object)

    return temp_background

def apply_tint(image, tint_color):
    """Applies a tint color to the image"""
    tinted_image = Image.new("RGBA", image.size)
    pixels = image.load()
    tinted_pixels = tinted_image.load()

    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            tr, tg, tb = tint_color

            # Blend the tint color with the original original with an alpha channel
            if a == 0:
                tinted_pixels[i, j] = (0, 0, 0, 0)  # To preserve transparency
            else:
                alpha = a / 255.0
                new_r = int((1 - alpha) * r + alpha * tr)
                new_g = int((1 - alpha) * g + alpha * tg)
                new_b = int((1 - alpha) * b + alpha * tb)
                tinted_pixels[i, j] = (new_r, new_g, new_b, a)

    return tinted_image

# Usage
place_object_and_score()