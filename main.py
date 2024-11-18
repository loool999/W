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