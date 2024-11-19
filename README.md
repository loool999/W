# Random Image Recreation Progrom Creating Images with Images 

This project places images onto another image at random positions, sizes, rotations, and tints, to remake the target image. The goal is to find the object placement, size, rotation, and tint that is closest to the target image.

<sub> litterly that thing that spu7nix made but worse</sub>

## How it Works

The script `main.py` performs the following actions:

1. **Loads Images:** Loads a background image (`background_path`), a set of objects images from the `/object/` folder, and tries to recreate the target image (`image_path`).

2. **Random Transformations:** For each attempt:
    * Randomly selects an object image from `/object/`.
    * Resizes the object to a random scale (`size_min` to `size_max`).
    * Rotates the object by a random angle (0 to 360 degrees).
    * Applies a random tint to the object.
    * Places the transformed object at a random position on the image.

3. **Score Calculation:** Calculates a score using the `image_color_difference` function from `dif.py`, comparing the modified background image with the `new bacground image`. This function uses a colormap to visualize the differences and calculates a score based on pixel-wise color distances.

4. **Output:**  Saves each modified background image and its corresponding difference colormap to a directory named `{attempt_number}_{score}` within the `/output/` folder. Also creates a `highest_score.json` file in the `/output/` directory containing the attempt number and score of the highest-scoring placement.

## Requirements

* Python 3.12.1 
* A CPU I guess
* No GPU cuz I dont have one ;-;

## Usage

1. **Clone the repository:** `git clone https://github.com/loool999/W`
2. **Install dependencies:** `pip install pillow matplotlib numpy`
3. **Prepare your images:**
    * Place your background image in the `background_path`.
    * Place your object images (PNG format) in the `/object/` folder.
    * Place your target image in the `image_path`.
4. **Run the script:** `python main.py`
5. **Customize:**  You can adjust parameters like `max_attempts` within the `main.py` script.

## Contributing

Contributions are welcome!  Please open an issue or submit a pull request.

## TODO
- Uhhh more thing
- Change name

## License
Used MIT LICENSE cuz that one looks pretty cool :)
