
"""
Wedge Wheel Center Analysis

Compare the central regions of two rasterized
wheel images using nearest-neighbor pixel replication.

No interpolation or smoothing is applied.
"""

from pathlib import Path

import numpy as np
from PIL import Image


OUTPUT_DIR = Path(__file__).resolve().parent

CENTER_X = 400
CENTER_Y = 300

HALF_SIZE = 40
ZOOM_FACTOR = 5
GAP = 30


def extract_center(image_array):
    """Extract an 80 x 80 region around the wheel center."""

    return image_array[
        CENTER_Y - HALF_SIZE:CENTER_Y + HALF_SIZE,
        CENTER_X - HALF_SIZE:CENTER_X + HALF_SIZE
    ]


def pixel_zoom(image_array, factor):
    """Enlarge pixels without interpolation."""

    return np.repeat(
        np.repeat(image_array, factor, axis=0),
        factor,
        axis=1
    )


def main():

    images = []

    for k in [1, 8]:

        image_path = OUTPUT_DIR / f"experiment_3_wheel_k{k}.png"

        image_array = np.asarray(
            Image.open(image_path).convert("RGB")
        )

        center = extract_center(image_array)

        enlarged = pixel_zoom(center, ZOOM_FACTOR)

        images.append(enlarged)

        gray_pixels = np.count_nonzero(
            (center[:, :, 0] > 0) &
            (center[:, :, 0] < 255)
        )

        print(f"k={k}: Center Gray Pixels = {gray_pixels}")

    height, width = images[0].shape[:2]

    # Construct a side-by-side comparison image
    comparison = np.full(
        (height, width * 2 + GAP, 3),
        255,
        dtype=np.uint8
    )

    comparison[:, :width] = images[0]
    comparison[:, width + GAP:] = images[1]

    output_path = OUTPUT_DIR / "experiment_3_wheel_center_comparison.png"

    result = Image.fromarray(comparison)

    result.save(output_path)
    result.show()

    print("\nWheel Center Comparison")
    print("Left: k=1")
    print("Right: k=8")
    print("Zoom Factor:", ZOOM_FACTOR)
    print("Image Saved:", output_path)


if __name__ == "__main__":
    main()
