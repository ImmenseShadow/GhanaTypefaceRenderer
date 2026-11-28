# ANANSE Typeface Renderer

A Python renderer that reads the ANANSE TrueType font, extracts a character's vector outline, approximates its Bézier curves with line segments, and rasterizes the outline into a grayscale PNG.

## Project structure

- `main.py`: command-line entry point. Coordinates the rendering pipeline.
- `fonts/Ananse-Regular-4.ttf`: the ANANSE font used for rendering.
- `renderer/font_loader.py`: opens the font and maps a Unicode character to its glyph.
- `renderer/bezier.py`: evaluates linear, quadratic, and cubic Bézier equations.
- `renderer/flattening.py`: uses FontTools' drawing pen interface to turn glyph curves into point contours.
- `renderer/winding.py`: calculates scan-line intersections and winding-number changes.
- `renderer/rasterizer.py`: fills pixels using the non-zero winding rule.
- `output/`: destination for rendered PNG images.
- `tests/`: automated tests.

## Requirements

- Python 3.10 or newer
- FontTools
- NumPy
- Pillow

Install dependencies from the project root in PowerShell:

```powershell
py -m pip install -r requirements.txt
```

## Render a character

Run these commands from the repository's root directory:

```powershell
py main.py --char A
py main.py --char Ɛ --output output/open_e.png
py main.py --char 8 --size 500 --steps 24
```

The default font path is already set to `fonts/Ananse-Regular-4.ttf`. To use another font, provide `--font path/to/font.ttf`.

The renderer saves a grayscale PNG in `output/glyph.png` by default. Black is the background and white is the glyph.

## Test the project

```powershell
py -m unittest discover -s tests -v
```

## Font inventory verified

The committed ANANSE font contains **84 glyph slots**: the `.notdef` glyph, the space glyph, and 82 visible character glyphs. Its Unicode character map contains 83 entries including space.

- Latin uppercase: A-Z
- Latin lowercase: a-z
- Digits: 0-9
- Ghanaian characters: Ɛ, ɛ, Ɔ, ɔ
- Punctuation and operators: ! ( ) + , - . : ; = ? [ ] × ÷ −
- Space: a spacing glyph with no filled outline

The renderer can process every character in this font's Unicode character map. The space character is expected to produce no filled bitmap because it has advance width but no outline.

## Current renderer scope and limitations

- Reads TrueType/OpenType fonts through FontTools.
- Extracts glyph contours, including composite glyph components.
- Samples quadratic and cubic Bézier curves using a fixed number of steps.
- Converts font coordinates into image pixel coordinates.
- Rasterizes contours with scan lines and the non-zero winding rule, preserving holes when contour directions are correct.
- Produces binary coverage in a grayscale PNG. Anti-aliasing/supersampling is a separate enhancement.
- Renders one character at a time. Text shaping, kerning, word layout, and line wrapping are not implemented.

The `--size` value sets the scale relative to the font's em square, so the final image width and height vary with each character's proportions.
