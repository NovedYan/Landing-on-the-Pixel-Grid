
"""
Supersampling Performance Benchmark

Measure the rendering cost of different
supersampling factors on the same output canvas.

Each factor is measured three times.
The median execution time is reported.
"""

import csv
import statistics
import time

from pathlib import Path

from geometry import create_pentagram, rotate_path
from supersampling import render_supersampled


WIDTH = 800
HEIGHT = 600

FACTORS = [1, 2, 4, 8]
REPEATS = 3

OUTPUT_DIR = Path(__file__).resolve().parent


def main():

    # 使用相同幾何形狀，確保比較公平
    star = rotate_path(
        create_pentagram(),
        5
    )

    results = []

    print("Supersampling Performance Benchmark")
    print(f"Output Canvas: {WIDTH} x {HEIGHT}")
    print(f"Repeats: {REPEATS}")

    for k in FACTORS:

        measurements = []
        filled_samples = 0

        for run in range(REPEATS):

            # Measure the complete rendering pipeline
            start = time.perf_counter()

            canvas, filled_samples = render_supersampled(
                [star],
                WIDTH,
                HEIGHT,
                k=k
            )

            elapsed = time.perf_counter() - start

            assert canvas.shape == (HEIGHT, WIDTH, 3)

            measurements.append(elapsed)

        median_time = statistics.median(measurements)

        print(f"\nk = {k}")
        print(f"High Resolution: {WIDTH*k} x {HEIGHT*k}")
        print(f"Filled Samples: {filled_samples}")
        print(f"Run Times: {[round(t, 4) for t in measurements]}")
        print(f"Median Time: {median_time:.4f} seconds")

        results.append([
            k,
            WIDTH,
            HEIGHT,
            WIDTH * k,
            HEIGHT * k,
            filled_samples,
            round(median_time, 6),
            *[round(t, 6) for t in measurements]
        ])

    # Export the measured data
    output_path = OUTPUT_DIR / "experiment_2_render_times.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "factor",
            "output_width",
            "output_height",
            "high_width",
            "high_height",
            "filled_samples",
            "median_seconds",
            "run1_seconds",
            "run2_seconds",
            "run3_seconds"
        ])

        writer.writerows(results)

    print("\nBenchmark Completed")
    print("Results Saved:", output_path)


if __name__ == "__main__":
    main()
