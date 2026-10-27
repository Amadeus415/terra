#!/usr/bin/env python3
"""Static 2D support margin for the *reference CAD pose*, not a walking controller.

Coordinates are millimeters in Fusion's X-Z ground plane. Feet are bounding-box
centers from the reference TPU bodies, not measured contact patches. The user
must supply the combined robot's measured projected center of mass.
"""
import argparse
import math

# X-Z centers of the four TPU contact body bounding boxes in the reference pose.
FEET = {
    "positive_x_positive_z": (89.0, 102.35),
    "negative_x_positive_z": (-89.0, 102.35),
    "positive_x_negative_z": (89.0, -91.25),
    "negative_x_negative_z": (-89.0, -91.25),
}


def cross(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def convex_hull(points):
    points = sorted(set(points))
    if len(points) < 3:
        raise ValueError("At least three distinct support points are required")
    lower = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    hull = lower[:-1] + upper[:-1]
    if len(hull) < 3:
        raise ValueError("Support points are collinear")
    return hull


def margin_mm(points, projected_com):
    """Smallest signed distance to a hull edge; negative means outside."""
    hull = convex_hull(points)
    return min(
        cross(a, b, projected_com) / math.dist(a, b)
        for a, b in zip(hull, hull[1:] + hull[:1])
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("x_mm", type=float, help="projected center of mass X, mm")
    parser.add_argument("z_mm", type=float, help="projected center of mass Z, mm")
    args = parser.parse_args()
    if not math.isfinite(args.x_mm) or not math.isfinite(args.z_mm):
        parser.error("center-of-mass coordinates must be finite")
    p = (args.x_mm, args.z_mm)
    print("Illustrative static CAD-pose check; not physical validation.")
    print(f"All four feet: {margin_mm(FEET.values(), p):+.2f} mm")
    for lifted in FEET:
        points = [p for name, p in FEET.items() if name != lifted]
        print(f"With {lifted} lifted: {margin_mm(points, p):+.2f} mm")
    print("Positive = inside; zero = boundary; negative = outside.")
    print("Assumes coplanar fixed point contacts and vertical gravity; no dynamics or friction.")


if __name__ == "__main__":
    main()
