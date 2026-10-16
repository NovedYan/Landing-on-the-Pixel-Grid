
"""
Geometry Utilities

Construct and transform geometric paths.

Features:
    - Five-vertex self-intersecting pentagram
    - Rotation around an arbitrary center

No built-in drawing or rasterization functions are used.
"""

import math


# ==========================================
# Pentagram Construction
# ==========================================

def create_pentagram(cx=400, cy=300, radius=220):
    """
    Create a five-pointed self-intersecting star.

    Vertices are visited in every-second-point order.
    """

    vertices = []

    for i in range(5):

        angle = -math.pi / 2 + i * 2 * math.pi / 5

        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)

        vertices.append((x, y))

    visiting_order = [0, 2, 4, 1, 3]

    return [vertices[i] for i in visiting_order]


# ==========================================
# Geometric Rotation
# ==========================================

def rotate_path(path, angle_degrees, center=(400, 300)):
    """
    Rotate a geometric path around a specified center.

    Screen coordinates:
        X increases rightward.
        Y increases downward.

    Positive angles appear clockwise on screen.
    """

    theta = math.radians(angle_degrees)

    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    cx, cy = center

    rotated = []

    for x, y in path:

        # Translate point relative to rotation center
        dx = x - cx
        dy = y - cy

        # Apply 2D rotation matrix
        rx = dx * cos_theta - dy * sin_theta
        ry = dx * sin_theta + dy * cos_theta

        # Translate back to original coordinate system
        rotated.append((cx + rx, cy + ry))

    return rotated
