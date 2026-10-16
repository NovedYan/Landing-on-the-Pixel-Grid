
"""
Landing on the Pixel Grid
Unified Experiment Runner

Execute the complete experiment pipeline with
a single command.

Each experiment remains independently executable.
Results are saved in the project directory.

Usage:
    python run_all.py
"""

import os
import subprocess
import sys
import time

from pathlib import Path


# ==========================================
# Project Configuration
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent


# ==========================================
# Experiment Execution Order
# ==========================================

EXPERIMENTS = [
    ("Star Supersampling", "main.py"),
    ("Performance Benchmark", "benchmark.py"),
    ("Performance Visualization", "plot_benchmark.py"),
    ("Edge Intensity Profile", "edge_profile.py"),
    ("High-Frequency Wedge Wheel", "wheel_experiment.py"),
    ("Wheel Center Analysis", "wheel_center_analysis.py"),
]


# ==========================================
# Unified Experiment Runner
# ==========================================

def main():

    total_start = time.perf_counter()

    print("=" * 60)
    print("LANDING ON THE PIXEL GRID")
    print("Unified Experiment Runner")
    print("=" * 60)

    # Use the current Python environment
    python_executable = sys.executable

    # Configure non-blocking Matplotlib output.
    # Charts are still saved as PNG files.
    environment = os.environ.copy()
    environment["MPLBACKEND"] = "Agg"

    for index, (name, filename) in enumerate(EXPERIMENTS, start=1):

        script_path = PROJECT_DIR / filename

        if not script_path.is_file():
            print(f"\nERROR: Missing script: {filename}")
            return

        print(f"\n[{index}/{len(EXPERIMENTS)}] {name}")
        print(f"Running: {filename}")
        print("-" * 60, flush=True)

        start = time.perf_counter()

        try:
            subprocess.run(
                [python_executable, str(script_path)],
                cwd=PROJECT_DIR,
                env=environment,
                check=True
            )

        except subprocess.CalledProcessError as error:
            print(f"\nFAILED: {filename}")
            print(f"Exit Code: {error.returncode}")
            print("Execution stopped.")
            return

        elapsed = time.perf_counter() - start

        print(f"COMPLETED: {name}")
        print(f"Elapsed Time: {elapsed:.3f} seconds", flush=True)

    total_elapsed = time.perf_counter() - total_start

    print("\n" + "=" * 60)
    print("ALL EXPERIMENTS COMPLETED")
    print("=" * 60)
    print(f"Total Execution Time: {total_elapsed:.3f} seconds")
    print(f"Output Directory: {PROJECT_DIR}")


if __name__ == "__main__":
    main()
