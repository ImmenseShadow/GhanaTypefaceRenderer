from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("output")
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

CELL_WIDTH = 150
CELL_HEIGHT = 180
COLUMNS = 6
ROWS = 5

sheet = Image.new(
    "RGB",
    (COLUMNS * CELL_WIDTH, ROWS * CELL_HEIGHT),
    "white"
)

draw = ImageDraw.Draw(sheet)
label_font = ImageFont.truetype("arial.ttf", 18)

for index, char in enumerate(CHARACTERS):
    row = index // COLUMNS
    col = index % COLUMNS

    path = OUTPUT_DIR / f"U+{ord(char):04X}.png"
    glyph = Image.open(path).convert("L")

    glyph.thumbnail((110, 125))

    x = col * CELL_WIDTH + (CELL_WIDTH - glyph.width) // 2
    y = row * CELL_HEIGHT + 10

    sheet.paste(glyph.convert("RGB"), (x, y))

    label = draw.textbbox((0, 0), char, font=label_font)
    label_width = label[2] - label[0]

    draw.text(
        (col * CELL_WIDTH + (CELL_WIDTH - label_width) // 2,
         row * CELL_HEIGHT + 140),
        char,
        fill="black",
        font=label_font
    )

sheet.save(OUTPUT_DIR / "uppercase_contact_sheet.png")
print("Saved: output/uppercase_contact_sheet.png")