"""
NON-ZERO WINDING RULE
Purpose:
    Find where a horizontal scan line crosses polygon contour edges and
    record each crossing's winding contribution.

Algorithm steps:
    1. Visit every edge in every contour, including the closing edge.
    2. Ignore horizontal edges because they do not cross a horizontal scan line.
    3. Use a half-open y interval to avoid counting shared vertices twice.
    4. Calculate the x coordinate where each crossing occurs.
    5. Record +1 for one edge direction and -1 for the opposite direction.
    6. During rasterization, accumulate these values from left to right.
       A point is inside when the accumulated winding number is not zero.

The sign convention is not important by itself; consistent opposite contour
directions are what allow holes to cancel under the non-zero rule.
"""


def scanline_intersections(contours, scan_y):
    """Return sorted-ready (x_intersection, winding_delta) events."""
    intersections = []

    for contour in contours:
        if len(contour) < 2:
            continue

        for index in range(len(contour)):
            x1, y1 = contour[index]
            x2, y2 = contour[(index + 1) % len(contour)]

            # Ignore horizontal edges.
            if y1 == y2:
                continue

            # Downward crossing in image coordinates.
            if y1 <= scan_y < y2:
                t = (scan_y - y1) / (y2 - y1)
                x_intersection = x1 + t * (x2 - x1)
                intersections.append((x_intersection, 1))

            # Upward crossing in image coordinates.
            elif y2 <= scan_y < y1:
                t = (scan_y - y1) / (y2 - y1)
                x_intersection = x1 + t * (x2 - x1)
                intersections.append((x_intersection, -1))

    intersections.sort(key=lambda event: event[0])
    return intersections
