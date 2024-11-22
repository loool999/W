import os
import random
import json
from PIL import Image
from dif import image_color_difference

# |------|Variables|------|
BACKGROUND_PATH = "filled.jpg"
OBJECT_FOLDER = "object"
OUTPUT_FOLDER = "output"
IMAGE_PATH = "image.jpg"
SIZE_MIN = 0.25
SIZE_MAX = 4
MAX_ATTEMPTS = 100
GENERATIONS = 10
CHILDREN = 5  # Number of children per generation
SURVIVORS = 10 # Number of survivors to save

# |------|Functions|------|
def main():
    for generation_number in range(GENERATIONS):
        generation_output = os.path.join(OUTPUT_FOLDER, f"generation_{generation_number + 1}")
        if not os.path.exists(generation_output):
            os.makedirs(generation_output)

        top_children = []

        for attempt_number in range(MAX_ATTEMPTS):
            object_file = random.choice([f for f in os.listdir(OBJECT_FOLDER) if f.endswith('.png')])
            object_path = os.path.join(OBJECT_FOLDER, object_file)
            object_image = Image.open(object_path).convert("RGBA")

            modified_background, object_data = place_object_random(Image.open(BACKGROUND_PATH).convert("RGBA"), object_image, object_file)

            # Create directory for this child *before* saving the image
            child_output_dir = os.path.join(generation_output, f"{generation_number + 1}_{attempt_number + 1}")  # Temporary name
            os.makedirs(child_output_dir)  # Create the directory

            modified_background_path = os.path.join(child_output_dir, f"modified_{attempt_number + 1}.png")
            modified_background.save(modified_background_path)

            try:
                score = image_color_difference(modified_background_path, IMAGE_PATH)
            except Exception as e:
                print(f"Error in image_color_difference: {e}")
                score = -1  # Or handle the error differently

            # Rename the directory *after* calculating the score
            new_child_output_dir = os.path.join(generation_output, f"{generation_number + 1}_{attempt_number + 1}_{score}")
            os.rename(child_output_dir, new_child_output_dir)
            child_output_dir = new_child_output_dir  # Update the variable

            # Colormap saving (add error handling here too if needed)
            colormap_path = os.path.join(child_output_dir, "difference_colormap.png")
            if os.path.exists("difference_colormap.png"):
                os.rename("difference_colormap.png", colormap_path)

            print(f"Generation {generation_number + 1}, Attempt {attempt_number + 1}: Score = {score}, saved in {child_output_dir}")

            top_children.append({
                "score": score,
                "attempt_number": attempt_number + 1,
                "modified_path": modified_background_path,
                "colormap_path": colormap_path  # Store the correct colormap path
            })

        top_children.sort(key=lambda x: x["score"], reverse=True)
        for i in range(len(top_children)):
            if i >= CHILDREN:
                try:
                    os.remove(top_children[i]['modified_path'])
                    if os.path.exists(top_children[i]['colormap_path']):
                        os.remove(top_children[i]['colormap_path'])
                    os.rmdir(os.path.dirname(top_children[i]['modified_path'])) # Remove the now empty directory
                except OSError as e:
                    print(f"Error removing extra files/directories: {e}")


def place_object_random(background, object_image, object_file):
    bg_w, bg_h = background.size
    obj_w, obj_h = object_image.size

    scale_factor = random.uniform(SIZE_MIN, SIZE_MAX)
    new_obj_w = int(obj_w * scale_factor)
    new_obj_h = int(obj_h * scale_factor)
    resized_object = object_image.resize((new_obj_w, new_obj_h), Image.LANCZOS)

    angle = random.uniform(0, 360)
    rotated_object = resized_object.rotate(angle, expand=True)

    tint_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tinted_object = apply_tint(rotated_object, tint_color)

    rot_w, rot_h = tinted_object.size
    x = random.randint(-rot_w // 2, bg_w - rot_w // 2)
    y = random.randint(-rot_h // 2, bg_h - rot_h // 2)

    temp_background = Image.new("RGBA", background.size)
    temp_background.paste(background, (0, 0))
    temp_background.paste(tinted_object, (x, y), tinted_object)

    return temp_background, {
        "object_name": object_file,  # Use object_file directly
        "rotation_angle": angle,
        "tint_color": tint_color,
        "scale_factor": scale_factor,
        "position": (x, y)
    }

def apply_tint(image, tint_color):
    """Applies a tint color to the image"""
    tinted_image = Image.new("RGBA", image.size)
    pixels = image.load()
    tinted_pixels = tinted_image.load()

    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            tr, tg, tb = tint_color

            if a == 0:
                tinted_pixels[i, j] = (0, 0, 0, 0)
            else:
                alpha = a / 255.0
                new_r = int((1 - alpha) * r + alpha * tr)
                new_g = int((1 - alpha) * g + alpha * tg)
                new_b = int((1 - alpha) * b + alpha * tb)
                tinted_pixels[i, j] = (new_r, new_g, new_b, a)

    return tinted_image

def place_object_from_data(background, object_data):
    object_path = os.path.join(OBJECT_FOLDER, object_data["object_name"])
    object_image = Image.open(object_path).convert("RGBA")

    # Apply transformations using object_data
    scale_factor = object_data["scale_factor"]
    obj_w, obj_h = object_image.size
    resized_object = object_image.resize((int(obj_w * scale_factor), int(obj_h * scale_factor)), Image.LANCZOS)

    rotated_object = resized_object.rotate(object_data["rotation_angle"], expand=True)
    tinted_object = apply_tint(rotated_object, object_data["tint_color"])

    x, y = object_data["position"]

    temp_background = Image.new("RGBA", background.size)
    temp_background.paste(background, (0, 0))
    temp_background.paste(tinted_object, (x, y), tinted_object)
    return temp_background

# |------|Usage|------|
if __name__ == "__main__":
    main()