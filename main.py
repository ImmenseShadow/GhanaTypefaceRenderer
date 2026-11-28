"""
GHANA TYPEFACE RENDERER
Purpose:
    Load a font, extract one glyph's outline, flatten its curves, and rasterize it.

Algorithm steps:
    1. Read the font path, character, output size, and curve sampling setting.
    2. Load the font and find the glyph that represents the requested character.
    3. Extract the glyph outline and approximate its curves with line segments.
    4. Find the outline's bounding box and convert font units into pixel coordinates.
    5. Rasterize the contours using scan lines and the non-zero winding rule.
    6. Save the resulting grayscale bitmap as a PNG image.

The functions used here are implemented in the renderer package.
"""

import argparse
import math
from pathlib import Path

from PIL import Image

from renderer.font_loader import FontLoader
from renderer.flattening import flatten_glyph
from renderer.rasterizer import rasterize_contours


def convert_to_pixel_coordinates(contours, units_per_em, pixel_size, padding):
    """Convert font-unit coordinates (y increases upward) into image coordinates."""
    all_points = [point for contour in contours for point in contour]

    if not all_points:
        return [], 2 * padding, 2 * padding

    min_x = min(point[0] for point in all_points)
    max_x = max(point[0] for point in all_points)
    min_y = min(point[1] for point in all_points)
    max_y = max(point[1] for point in all_points)

    # Scale relative to the font's em square, preserving the glyph proportions.
    scale = pixel_size / units_per_em

    width = max(1, math.ceil((max_x - min_x) * scale)) + 2 * padding
    height = max(1, math.ceil((max_y - min_y) * scale)) + 2 * padding

    pixel_contours = []
    for contour in contours:
        pixel_contour = []
        for x, y in contour:
            pixel_x = (x - min_x) * scale + padding
            # Image coordinates start at the top, so invert the font's y-axis.
            pixel_y = (max_y - y) * scale + padding
            pixel_contour.append((pixel_x, pixel_y))
        pixel_contours.append(pixel_contour)

    return pixel_contours, width, height


def main():
    parser = argparse.ArgumentParser(
        description="Render one character from the ANANSE TTF/OTF font."
    )
    parser.add_argument(
        "--font",
        default="fonts/Ananse-Regular-4.ttf",
        help="Path to a .ttf or .otf font",
    )
    parser.add_argument("--char", default="A", help="Single character to render")
    parser.add_argument("--size", type=int, default=400,
                        help="Approximate em-square scale in pixels")
    parser.add_argument("--steps", type=int, default=16,
                        help="Samples per Bézier curve")
    parser.add_argument("--padding", type=int, default=20,
                        help="Image padding in pixels")
    parser.add_argument("--output", default="output/glyph.png",
                        help="Output PNG path")
    args = parser.parse_args()

    if len(args.char) != 1:
        parser.error("--char must contain exactly one character")

    if args.size <= 0 or args.steps < 1 or args.padding < 0:
        parser.error("--size and --steps must be positive; --padding cannot be negative")

    font_path = Path(args.font)
    if not font_path.is_file():
        raise FileNotFoundError(
            f"Font not found: {font_path}\n"
            "Check the --font path. The repository's ANANSE font is "
            "'fonts/Ananse-Regular-4.ttf'."
        )

    with FontLoader(font_path) as font:
        glyph_name, glyph, glyph_set = font.get_glyph(args.char)
        contours = flatten_glyph(glyph_name, glyph_set, steps=args.steps)

        if not contours or not any(len(contour) >= 3 for contour in contours):
            print(
                f"{args.char!r} maps to {glyph_name!r}, "
                "but has no filled outline (this is normal for space)."
            )
            return

        pixel_contours, width, height = convert_to_pixel_coordinates(
            contours, font.units_per_em, args.size, args.padding
        )
        bitmap = rasterize_contours(pixel_contours, width, height)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(bitmap, mode="L").save(output_path)

    print(f"Rendered {args.char!r} using glyph {glyph_name!r}")
    print(f"Image dimensions: {width} x {height}")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
