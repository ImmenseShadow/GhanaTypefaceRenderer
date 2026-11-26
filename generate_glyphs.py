#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image, ImageDraw, ImageFont

GROUPS = {
    "uppercase": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "lowercase": list("abcdefghijklmnopqrstuvwxyz"),
    "digits": list("0123456789"),
    "ghanaian": ["Ɛ", "ɛ", "Ɔ", "ɔ"],
    "punctuation": list(".,:;!?-()[]"),
    "arithmetic": ["+", "−", "×", "÷", "="],
    "quotes": ["'", '"'],
    "slashes": ["/", "\\"],
    "symbols": list("@#$%^&*"),
}
GLYPHS = [(group, ch) for group, chars in GROUPS.items() for ch in chars]
CONFIRMED_ADINKRA = {
    "A": "Afa", "B": "Mpuaknum", "C": "Sankofa",
    "O": "Akoma", "o": "Akoma",
    "J": "Owuo Atwedee", "j": "Owuo Atwedee",
}
PROPOSED_ADINKRA = {"D": "Dwennimmen", "E": "Eban", "F": "Fawohodie"}

def glyph_name(ch):
    return f"U+{ord(ch):04X}"

def make_svg(font, cmap, glyph_set, ch, out_path):
    name = cmap.get(ord(ch))
    if name is None:
        raise ValueError(f"Font has no cmap entry for {ch!r} ({glyph_name(ch)}).")
    pen = SVGPathPen(glyph_set)
    glyph_set[name].draw(pen)
    path_data = pen.getCommands()
    units = font["head"].unitsPerEm
    advance = font["hmtx"].metrics[name][0]
    padding = units * 0.08
    width = max(advance, units * 0.4) + 2 * padding
    height = units + 2 * padding
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">
  <title>{escape(ch)} ({glyph_name(ch)})</title>
  <metadata>ANANSE export. Source glyph: {escape(name)}. Adinkra integration requires review.</metadata>
  <g transform="translate({padding:.2f},{units + padding:.2f}) scale(1,-1)">
    <path d="{path_data}" fill="#000000" fill-rule="nonzero"/>
  </g>
</svg>
'''
    out_path.write_text(svg, encoding="utf-8")

def write_manifest(out_dir):
    records = []
    for group, ch in GLYPHS:
        symbol = CONFIRMED_ADINKRA.get(ch, PROPOSED_ADINKRA.get(ch, ""))
        status = ("confirmed mapping" if ch in CONFIRMED_ADINKRA else
                  "proposed mapping; approval required" if ch in PROPOSED_ADINKRA else
                  "mapping not assigned")
        records.append({
            "character": ch, "codepoint": glyph_name(ch), "group": group,
            "adinkra_symbol": symbol, "mapping_status": status,
            "geometry_status": "NOT VERIFIED / NOT INTEGRATED BY EXPORTER",
            "svg_file": f"glyphs/{glyph_name(ch)}.svg",
        })
    (out_dir / "glyph_manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "glyph_manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def make_contact_sheet(font_path, out_dir):
    try:
        label_font = ImageFont.truetype(str(font_path), 17)
        glyph_font = ImageFont.truetype(str(font_path), 72)
    except Exception:
        label_font, glyph_font = ImageFont.load_default(), ImageFont.load_default()
    cell_w, cell_h, cols = 190, 145, 6
    rows = (len(GLYPHS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (group, ch) in enumerate(GLYPHS):
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        box = draw.textbbox((0, 0), ch, font=glyph_font)
        tw, th = box[2] - box[0], box[3] - box[1]
        draw.text((x + (cell_w - tw) / 2, y + 12 - box[1]), ch, fill="black", font=glyph_font)
        draw.text((x + 7, y + 112), f"{glyph_name(ch)}  {group}", fill="#555555", font=label_font)
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline="#dddddd")
    sheet.save(out_dir / "ANANSE_93_Glyph_Contact_Sheet.png", dpi=(300, 300))

def main():
    parser = argparse.ArgumentParser(description="Export ANANSE glyphs to SVG.")
    parser.add_argument("--font", default="fonts/ANANSE-Regular.ttf")
    parser.add_argument("--output", default="ANANSE_SVG_Output")
    args = parser.parse_args()
    font_path, out_dir = Path(args.font), Path(args.output)
    if not font_path.exists():
        raise SystemExit(f"Font not found: {font_path}. Run from the renderer folder or pass --font.")
    out_dir.mkdir(parents=True, exist_ok=True)
    glyph_dir = out_dir / "glyphs"
    glyph_dir.mkdir(exist_ok=True)
    font = TTFont(str(font_path))
    cmap, glyph_set = font.getBestCmap(), font.getGlyphSet()
    failures = []
    for _, ch in GLYPHS:
        try:
            make_svg(font, cmap, glyph_set, ch, glyph_dir / f"{glyph_name(ch)}.svg")
        except Exception as exc:
            failures.append((ch, str(exc)))
    write_manifest(out_dir)
    make_contact_sheet(font_path, out_dir)
    print(f"Expected visible glyphs: {len(GLYPHS)}")
    print(f"SVG files generated: {len(GLYPHS) - len(failures)}")
    print(f"Failures: {len(failures)}")
    print(f"Output: {out_dir.resolve()}")
    for ch, error in failures:
        print(f"FAILED {ch!r}: {error}")
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
