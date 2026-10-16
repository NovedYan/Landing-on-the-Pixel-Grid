
"""
Landing on the Pixel Grid

Experiment 1: Rotated Pentagram Rasterization

Create a five-pointed star, rotate its geometry,
and rasterize it with the non-zero winding rule.

Baseline resolution: 800 x 600
Supersampling factor: k = 1
"""

from pathlib import Path

import numpy as np
from PIL import Image

from geometry import create_pentagram, rotate_path
from rasterizer import fill_nonzero_winding

from supersampling import render_supersampled

WIDTH = 800
HEIGHT = 600

OUTPUT_DIR = Path(__file__).resolve().parent


def main():

    # Create a white RGB pixel array
    canvas = np.full(
        (HEIGHT, WIDTH, 3),
        255,
        dtype=np.uint8
    )

    # Generate a self-intersecting pentagram
    star = create_pentagram()

    # Rotate the original geometry by 5 degrees
    rotated_star = rotate_path(star, 5)

    # Rasterize at the original resolution (k = 1)
    filled_pixels = fill_nonzero_winding(
        canvas,
        [rotated_star]
    )

    # ==========================================
    # Save and Preview the Rendered Image
    # ==========================================

    output_path = OUTPUT_DIR / "experiment_1_star_k1.png"

    # Convert the pixel array to a Pillow image
    image = Image.fromarray(canvas)

    # Save the experiment result
    image.save(output_path)

    # Automatically open the image viewer
    image.show()
    
    print("Rotated Pentagram Rasterization")
    print("Rotation: 5 degrees")
    print("Supersampling Factor: 1")
    print("Canvas: 800 x 600")
    print("Filled Pixels:", filled_pixels)
    print("Image Saved:", output_path)
    
    
    
    # ==========================================
    # Supersampling Comparison
    # ==========================================

    # Test increasing sampling densities
    sampling_factors = [2, 4, 8]

    for k in sampling_factors:

        aa_canvas, highres_pixels = render_supersampled(
            [rotated_star],
            WIDTH,
            HEIGHT,
            k=k
        )

        # Export the rasterized result
        aa_path = OUTPUT_DIR / f"experiment_1_star_k{k}.png"

        aa_image = Image.fromarray(aa_canvas)
        aa_image.save(aa_path)
        aa_image.show()

        # Count pixels with intermediate grayscale values
        gray_pixels = np.count_nonzero(
            (aa_canvas[:, :, 0] > 0) &
            (aa_canvas[:, :, 0] < 255)
        )

        print(f"\nSupersampling Experiment: k={k}")
        print("High Resolution:", WIDTH * k, "x", HEIGHT * k)
        print("Output Resolution:", WIDTH, "x", HEIGHT)
        print("Filled High-Resolution Samples:", highres_pixels)
        print("Gray Edge Pixels:", gray_pixels)
        print("Image Saved:", aa_path)




if __name__ == "__main__":
    main()
