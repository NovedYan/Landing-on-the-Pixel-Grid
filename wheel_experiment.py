
"""
High-Frequency Wedge Wheel Experiment

Construct a radial wheel using independent
triangular subpaths with alternating gaps.

Compare binary pixel-center sampling (k=1)
against supersampling (k=8).

All coverage calculations use the custom
non-zero winding scanline rasterizer.
"""

import math
from pathlib import Path

import numpy as np
from PIL import Image

from supersampling import render_supersampled


# ==========================================
# Experiment Configuration
# ==========================================

WIDTH = 800
HEIGHT = 600

CENTER_X = 400
CENTER_Y = 300

RADIUS = 245
WEDGE_COUNT = 48

FACTORS = [1, 8]

OUTPUT_DIR = Path(__file__).resolve().parent


# ==========================================
# Radial Wedge Geometry
# ==========================================

def create_wedge_wheel(cx, cy, radius, wedge_count):
    """
    Construct a wheel from independent triangles.

    Each wedge occupies half of its angular period.
    The other half is left empty.

    Every triangle is a separate closed subpath.
    """

    if wedge_count < 2 or radius <= 0:
        raise ValueError("Invalid wheel geometry.")

    wheel = []

    angle_step = 2 * math.pi / wedge_count

    # Equal angular width for wedges and gaps
    wedge_angle = angle_step / 2

    for i in range(wedge_count):

        start_angle = -math.pi / 2 + i * angle_step
        end_angle = start_angle + wedge_angle

        # Two outer vertices on the radius
        p1 = (
            cx + radius * math.cos(start_angle),
            cy + radius * math.sin(start_angle)
        )

        p2 = (
            cx + radius * math.cos(end_angle),
            cy + radius * math.sin(end_angle)
        )

        # Triangle pointing toward the wheel center
        triangle = [
            (cx, cy),
            p1,
            p2
        ]

        wheel.append(triangle)

    return wheel


# ==========================================
# Rendering Experiment
# ==========================================

def main():

    wheel = create_wedge_wheel(
        CENTER_X,
        CENTER_Y,
        RADIUS,
        WEDGE_COUNT
    )

    print("High-Frequency Wedge Wheel")
    print("Output Canvas:", WIDTH, "x", HEIGHT)
    print("Wedge Count:", len(wheel))
    print("Vertices Per Wedge:", 3)
    print("Sampling Factors:", FACTORS)

    for k in FACTORS:

        # Use the same geometric subpaths for both cases
        canvas, filled_samples = render_supersampled(
            wheel,
            WIDTH,
            HEIGHT,
            k=k
        )

        # Count partially covered output pixels
        gray_pixels = np.count_nonzero(
            (canvas[:, :, 0] > 0) &
            (canvas[:, :, 0] < 255)
        )

        output_path = OUTPUT_DIR / f"experiment_3_wheel_k{k}.png"

        image = Image.fromarray(canvas)

        image.save(output_path)
        image.show()

        print(f"\nWheel Rasterization: k={k}")
        print("High Resolution:", WIDTH * k, "x", HEIGHT * k)
        print("Filled Samples:", filled_samples)
        print("Gray Edge Pixels:", gray_pixels)
        print("Image Saved:", output_path)


if __name__ == "__main__":
    main()
