"""
SCAN-LINE RASTERIZER
Purpose:
    Convert flattened glyph contours into a grayscale pixel array.

Algorithm steps:
    1. Create a blank image buffer.
    2. Visit each horizontal scan line through the centre of each pixel row.
    3. Find all contour-edge intersections for that scan line.
    4. Sort intersections from left to right.
    5. Move across pixel centres, accumulating winding contributions.
    6. Set a pixel to white when the winding number is non-zero; otherwise
       leave it black.
    7. Return the completed grayscale image buffer.

This is a basic binary-coverage renderer. Supersampling and anti-aliasing can
be added by the integration stage.
"""

import numpy as np

from .winding import scanline_intersections


def rasterize_contours(contours, width, height):
    if width <= 0 or height <= 0:
        raise ValueError("Image width and height must be positive.")

    bitmap = np.zeros((height, width), dtype=np.uint8)

    for pixel_y in range(height):
        scan_y = pixel_y + 0.5
        intersections = scanline_intersections(contours, scan_y)

        event_index = 0
        winding_number = 0

        for pixel_x in range(width):
            pixel_center_x = pixel_x + 0.5

            # Apply every crossing at or to the left of this pixel centre.
            while (event_index < len(intersections)
                   and intersections[event_index][0] <= pixel_center_x):
                winding_number += intersections[event_index][1]
                event_index += 1

            if winding_number != 0:
                bitmap[pixel_y, pixel_x] = 255

    return bitmap
