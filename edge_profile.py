
"""
Edge Intensity Profile Analysis

Identify the shallowest edge of a rotated pentagram.

Sample a horizontal pixel row near one endpoint
of that edge and compare grayscale intensities
from k=1 and k=8 supersampling.

The image data comes from the custom rasterizer.
"""

import csv
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from geometry import create_pentagram, rotate_path
from rasterizer import scanline_intersections


OUTPUT_DIR = Path(__file__).resolve().parent

IMAGE_K1 = OUTPUT_DIR / "experiment_1_star_k1.png"
IMAGE_K8 = OUTPUT_DIR / "experiment_1_star_k8.png"

PLOT_PATH = OUTPUT_DIR / "experiment_2_edge_profile.png"
CSV_PATH = OUTPUT_DIR / "experiment_2_edge_profile.csv"


def find_shallowest_edge(path):
    """Find the edge with the smallest absolute slope."""

    candidates = []

    for i in range(len(path)):

        a = path[i]
        b = path[(i + 1) % len(path)]

        dx = b[0] - a[0]
        dy = b[1] - a[1]

        if abs(dx) < 1e-12:
            continue

        slope = dy / dx

        candidates.append((abs(slope), i, a, b))

    _, index, a, b = min(candidates)

    return index, a, b


def main():

    # Reconstruct the same rotated geometry
    star = rotate_path(create_pentagram(), 5)

    edge_index, a, b = find_shallowest_edge(star)

    slope = (b[1] - a[1]) / (b[0] - a[0])

    # Choose the left endpoint as the starting reference
    left, right = sorted((a, b), key=lambda p: p[0])

    # Sample approximately 12% along the edge
    # to stay near an endpoint.
    t = 0.12

    target_y = left[1] + t * (right[1] - left[1])

    # Sample at the center of an integer pixel row
    row = round(target_y - 0.5)
    scan_y = row + 0.5

    # Find the geometric intersection on this row
    edge_x = (
        a[0]
        + (scan_y - a[1])
        * (b[0] - a[0])
        / (b[1] - a[1])
    )

    # Other path crossings are used to keep the
    # measurement window focused on this edge.
    crossings = scanline_intersections([star], scan_y)

    other_distances = [
        abs(x - edge_x)
        for x, _ in crossings
        if abs(x - edge_x) > 1e-5
    ]

    half_window = 30

    if other_distances:
        half_window = min(
            half_window,
            max(10, int(min(other_distances) / 2) - 2)
        )

    # Load previously rendered results
    image_k1 = np.asarray(Image.open(IMAGE_K1).convert("RGB"))
    image_k8 = np.asarray(Image.open(IMAGE_K8).convert("RGB"))

    assert image_k1.shape == image_k8.shape

    height, width = image_k1.shape[:2]

    assert 0 <= row < height

    center_x = math.floor(edge_x)

    x_start = max(0, center_x - half_window)
    x_end = min(width, center_x + half_window + 1)

    x_values = np.arange(x_start, x_end)

    # Images are grayscale: one channel is sufficient
    intensity_k1 = image_k1[row, x_start:x_end, 0]
    intensity_k8 = image_k8[row, x_start:x_end, 0]

    # Save raw measurements
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "x",
            "intensity_k1",
            "intensity_k8"
        ])

        for x, v1, v8 in zip(
            x_values,
            intensity_k1,
            intensity_k8
        ):
            writer.writerow([int(x), int(v1), int(v8)])

    # Create intensity comparison plot
    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.step(
        x_values,
        intensity_k1,
        where="mid",
        linewidth=2,
        label="k = 1 (Point Sampling)"
    )

    ax.plot(
        x_values,
        intensity_k8,
        marker=".",
        linewidth=2,
        label="k = 8 (Supersampling)"
    )

    ax.axvline(
        edge_x,
        color="gray",
        linestyle=":",
        label="Geometric Edge"
    )

    ax.set_title("Edge Intensity Profile - Rotated Pentagram")

    ax.set_xlabel("X Position Along Selected Pixel Row")
    ax.set_ylabel("Pixel Intensity (0=Black, 255=White)")

    ax.set_ylim(-10, 265)
    ax.set_xticks(x_values[::max(1, len(x_values) // 10)])

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(PLOT_PATH, dpi=180)

    # Report geometric and image measurements
    gray_count = np.count_nonzero(
        (intensity_k8 > 0) &
        (intensity_k8 < 255)
    )

    print("Edge Intensity Profile")
    print("Shallowest Edge Index:", edge_index)
    print(f"Edge Slope: {slope:.6f}")
    print("Sample Row:", row)
    print(f"Edge Crossing X: {edge_x:.3f}")
    print("Profile X Range:", x_start, "to", x_end - 1)
    print("k=1 Unique Intensities:", np.unique(intensity_k1))
    print("k=8 Gray Samples:", gray_count)
    print("CSV Saved:", CSV_PATH)
    print("Plot Saved:", PLOT_PATH)

    plt.show()


if __name__ == "__main__":
    main()
