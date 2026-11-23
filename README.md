# Ghana Typeface Renderer

A learning-oriented glyph renderer using Python, FontTools, NumPy, and Pillow.

## Setup

From the project root, install dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy a `.ttf` or `.otf` font into the `fonts` directory. For example:

```text
fonts/
    YourFont.ttf
```

Run the renderer:

```bash
python main.py --font fonts/YourFont.ttf --char A
```

Choose another character or output size:

```bash
python main.py --font fonts/YourFont.ttf --char B --size 500 --output output/B.png
```

Run the Bézier tests:

```bash
python -m unittest discover -s tests -v
```

## Current implementation

- TTF/OTF loading and character mapping through FontTools.
- Quadratic and cubic Bézier evaluation.
- Curve flattening through sampled points.
- Scan-line rasterization.
- Non-zero winding fill rule.
- Grayscale PNG output.

## Important limitations

- Curve flattening currently uses a fixed number of samples per curve segment.
- Rasterization currently uses binary pixel coverage, not anti-aliasing.
- This is a first working baseline. It should be tested against the group's actual font and integrated with Member 8's supersampling stage.
- The current renderer renders one glyph at a time. Text layout, kerning, shaping, and line wrapping are outside this initial implementation.
