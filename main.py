from PIL import Image
import numpy as np

def load_and_resize_image(image_path, target_size=(256, 256)):
    """Load and resize an image to the target size."""
    img = Image.open(image_path).convert('RGB')
    return img.resize(target_size)

def calculate_color_difference(img1, img2):
    """Calculate the Euclidean color difference between two images."""
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    diff = np.sqrt(np.sum((arr1 - arr2) ** 2, axis=2))
    return diff

def map_difference_to_score(diff, score_map):
    """Map color differences to scores using a predefined score map."""
    mapped_scores = np.zeros_like(diff, dtype=int)
    for score, color_range in score_map.items():
        mapped_scores[(diff >= color_range[0]) & (diff < color_range[1])] = score
    return mapped_scores

def create_colormap_image(mapped_scores, color_map):
    """Create a color map image based on the mapped scores."""
    colormap_img = Image.new('RGB', mapped_scores.shape[::-1])
    pixels = colormap_img.load()
    for i in range(mapped_scores.shape[0]):
        for j in range(mapped_scores.shape[1]):
            score = mapped_scores[i, j]
            pixels[j, i] = color_map[score]
    return colormap_img

def save_colormap_image(colormap_img, score):
    """Save the color map image with a filename based on the score."""
    filename = f"colormap_score_{score}.png"
    colormap_img.save(filename)

def main(image1_path, image2_path):
    # Load and resize images
    img1 = load_and_resize_image(image1_path)
    img2 = load_and_resize_image(image2_path)

    # Calculate color difference
    diff = calculate_color_difference(img1, img2)

    # Define score map and color map
    score_map = {0: (0, 50), 50: (50, 100), 100: (100, 150), 150: (150, 256)}
    color_map = {0: (255, 0, 0), 50: (255, 165, 0), 100: (0, 255, 0), 150: (173, 216, 230)}

    # Map differences to scores
    mapped_scores = map_difference_to_score(diff, score_map)

    # Create color map image
    colormap_img = create_colormap_image(mapped_scores, color_map)

    # Calculate overall score (e.g., mean of mapped scores)
    overall_score = int(np.mean(mapped_scores))

    # Save color map image
    save_colormap_image(colormap_img, overall_score)

# Example usage
main("image1.jpg", "image2.jpg")
