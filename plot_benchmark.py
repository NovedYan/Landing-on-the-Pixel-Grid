
"""
Supersampling Performance Visualization

Load measured rendering times from CSV and
generate a reproducible performance chart.

Measurements are read from benchmark output.
No rendering benchmark is repeated here.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


OUTPUT_DIR = Path(__file__).resolve().parent

CSV_PATH = OUTPUT_DIR / "experiment_2_render_times.csv"
IMAGE_PATH = OUTPUT_DIR / "experiment_2_render_times.png"


def main():

    factors = []
    median_times = []

    # Read previously measured benchmark results
    with open(CSV_PATH, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            factors.append(int(row["factor"]))
            median_times.append(float(row["median_seconds"]))

    # Create the performance chart
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(
        factors,
        median_times,
        marker="o",
        linewidth=2,
        markersize=7,
        label="Measured Render Time"
    )

    # Display the measured value above each point
    for k, seconds in zip(factors, median_times):

        ax.annotate(
            f"{seconds:.4f} s",
            (k, seconds),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center"
        )

    ax.set_title(
        "Supersampling Performance Benchmark"
    )

    ax.set_xlabel("Supersampling Factor (k)")
    ax.set_ylabel("Median Render Time (seconds)")

    ax.set_xticks(factors)
    ax.set_ylim(bottom=0)

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    # Save the figure for reproducibility
    fig.savefig(IMAGE_PATH, dpi=180)

    print("Performance Visualization")
    print("Factors:", factors)
    print("Median Times:", median_times)
    print("Image Saved:", IMAGE_PATH)

    # Display the chart after saving
    plt.show()


if __name__ == "__main__":
    main()
