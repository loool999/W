import random
from PIL import Image
from tint import apply_tint

size_min=0.25
size_max=4

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