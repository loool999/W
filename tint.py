from PIL import Image

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