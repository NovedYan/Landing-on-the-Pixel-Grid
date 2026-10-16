
"""
Scanline Rasterizer

A custom non-zero winding number rasterization module.

Features:
    - Scanline intersection detection
    - Signed winding number accumulation
    - Multiple closed subpaths
    - Pixel-center coverage

All pixel coverage decisions are computed manually.
No built-in polygon filling or anti-aliasing is used.
"""

import math


# ==========================================
# Scanline Intersection Detection
# ==========================================

def scanline_intersections(subpaths, scan_y):
    """
    Find intersections between a scanline and closed paths.

    Coordinate system:
        X increases rightward.
        Y increases downward.

    Crossing direction:
        +1: downward edge
        -1: upward edge
    """

    intersections = []

    for path in subpaths:

        count = len(path)

        for i in range(count):

            x1, y1 = path[i]
            x2, y2 = path[(i + 1) % count]

            # Ignore horizontal edges
            if y1 == y2:
                continue

            # Half-open interval prevents duplicate crossings
            if not (min(y1, y2) <= scan_y < max(y1, y2)):
                continue

            # Calculate the intersection position
            x = x1 + (scan_y - y1) * (x2 - x1) / (y2 - y1)

            direction = 1 if y2 > y1 else -1

            intersections.append((x, direction))

    intersections.sort(key=lambda item: item[0])

    return intersections


# ==========================================
# Winding Number Calculation
# ==========================================

def winding_number_at_x(crossings, sample_x):
    """Calculate the signed winding number at sample_x."""

    winding = 0

    # 從左至右累加交點方向
    for crossing_x, direction in crossings:

        if crossing_x <= sample_x:
            winding += direction
        else:
            break

    return winding


# ==========================================
# Non-Zero Winding Fill
# ==========================================

def fill_nonzero_winding(canvas, subpaths, color=(0, 0, 0)):
    """
    Fill closed paths using the non-zero winding rule.

    Each row is processed independently.
    Pixel coverage is evaluated at pixel centers.
    """

    height, width = canvas.shape[:2]

    filled_pixels = 0

    for y in range(height):

        scan_y = y + 0.5

        crossings = scanline_intersections(
            subpaths,
            scan_y
        )

        winding = 0

        for i in range(len(crossings) - 1):

            current_x, direction = crossings[i]
            next_x = crossings[i + 1][0]

            winding += direction

            if winding == 0:
                continue

            # 將幾何區間轉換為像素索引
            x_start = max(
                0,
                math.ceil(current_x - 0.5)
            )

            x_end = min(
                width,
                math.ceil(next_x - 0.5)
            )

            if x_start < x_end:

                canvas[y, x_start:x_end] = color

                filled_pixels += x_end - x_start

    return filled_pixels
