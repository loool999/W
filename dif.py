from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
from concurrent.futures import ThreadPoolExecutor

def image_color_difference(image1_path, image2_path, output_path="difference_colormap.png", min_val=0, max_val=300):
    """
    Calculates and visualizes the color difference between two images using the 'jet' colormap
    and calculates a score for each pixel in the saved image based on its color.

    Args:
        image1_path (str): Path to the first image.
        image2_path (str): Path to the second image.
        output_path (str): Path to save the difference colormap.
        min_val (float): Minimum value for the color scale (maps to red in 'jet').
        max_val (float): Maximum value for the color scale.
    """
    try:
        # 1. Load Images and Convert to RGB
        img1 = Image.open(image1_path).convert("RGB")
        img2 = Image.open(image2_path).convert("RGB")

        # 2. Ensure Compatibility
        if img1.size != img2.size:
            raise ValueError("Images must be the same size.")

        # 3. Calculate Euclidean Distance
        arr1 = np.asarray(img1, dtype=np.float32)
        arr2 = np.asarray(img2, dtype=np.float32)
        diff = np.abs(arr1 - arr2)
        euclidean_dist = np.sqrt(np.sum(diff**2, axis=-1))

        # 4. Normalize and Apply Colormap
        normalized_diff = np.clip((euclidean_dist - min_val) / (max_val - min_val), 0, 1)
        cmap = matplotlib.cm.get_cmap('jet')
        colored_diff = (cmap(normalized_diff) * 255).astype(np.uint8)  # Apply colormap and convert to uint8

        # 5. Save Colormap
        plt.imsave(output_path, colored_diff)
        print(f"Difference colormap saved to {output_path}")

        # 6. Calculate Pixel Scores with Threaded Optimization
        total_score = calculate_pixel_scores_threaded(normalized_diff, min_val, max_val)

        # Display average difference
        average_difference = np.mean(euclidean_dist)
        print(f"Average Euclidean Distance: {average_difference}")

        return total_score

    except FileNotFoundError:
        print("Error: Image file not found.")
    except ValueError as e:
        print(f"Error: {e}")

def calculate_pixel_scores_threaded(normalized_diff, min_val, max_val):
    """
    Optimized pixel scoring with multi-threading.

    Args:
        normalized_diff (numpy.ndarray): The normalized difference array.
        min_val (float): Minimum value for the color scale.
        max_val (float): Maximum value for the color scale.

    Returns:
        float: Total score for pixels.
    """
    # Precompute the score range
    score_range = max_val - min_val

    # Divide the work into chunks for threading
    height, width = normalized_diff.shape
    step = height // 4  # Divide into 4 chunks for multi-threading

    def compute_chunk(start, end):
        # Calculate scores for the chunk
        reduced_chunk = normalized_diff[start:end:2, ::2]  # Every other pixel
        return np.sum(min_val + reduced_chunk * score_range)

    # Use ThreadPoolExecutor to compute chunks in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(compute_chunk, i, i + step) for i in range(0, height, step)]
        total_score = sum(f.result() for f in futures)

    return total_score

# Example Usage
total_score = image_color_difference("image.jpg", "filled.jpg", min_val=0, max_val=300)
print("Total Score:", total_score)
