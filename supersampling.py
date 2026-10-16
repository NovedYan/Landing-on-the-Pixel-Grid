
"""
Supersampling Utilities

Render geometric paths at a higher resolution,
then average subpixel blocks into the final image.

All pixel coverage decisions are computed by
the custom non-zero winding scanline rasterizer.
"""

import numpy as np

from rasterizer import fill_nonzero_winding


# ==========================================
# Supersampled Rasterization
# ==========================================

def render_supersampled(
    subpaths,
    width,
    height,
    k=2
):
    """
    Render closed geometric paths using supersampling.

    Parameters:
        subpaths: Closed polygonal paths.
        width: Output image width.
        height: Output image height.
        k: Supersampling factor.

    Returns:
        Final RGB image array.
        Number of filled high-resolution pixels.
    """

    if not isinstance(k, int) or k < 1:
        raise ValueError("Supersampling factor must be a positive integer.")

    # Allocate the high-resolution canvas
    high_width = width * k
    high_height = height * k

    high_canvas = np.full(
        (high_height, high_width, 3),
        255,
        dtype=np.uint8
    )

    # Scale the original geometric coordinates
    scaled_subpaths = [
        [(x * k, y * k) for x, y in path]
        for path in subpaths
    ]

    # Rasterize using our custom scanline algorithm
    filled_samples = fill_nonzero_winding(
        high_canvas,
        scaled_subpaths
    )

    # Group each k x k block into one output pixel
    blocks = high_canvas.reshape(
        height,
        k,
        width,
        k,
        3
    )

    # Average all subpixels to estimate area coverage
    final_canvas = np.rint(
        blocks.mean(axis=(1, 3))
    ).astype(np.uint8)

    return final_canvas, filled_samples
