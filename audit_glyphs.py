from fontTools.ttLib import TTFont
from pathlib import Path
import subprocess
import sys

FONT_PATH = Path("fonts/ANANSE-Regular.ttf")
OUTPUT_DIR = Path("output")

# Expected ANANSE character inventory: 93 visible glyphs
characters = (
        list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        + list("abcdefghijklmnopqrstuvwxyz")
        + list("0123456789")
        + list("ƐɛƆɔ")
        + list(".,:;!?()[]")
        + list("+-×÷=")
        + ["'", '"', "/", "\\"]
        + list("@#$%^&*")
)

font = TTFont(str(FONT_PATH))
cmap = font.getBestCmap() or {}

passed = []
missing = []
failed = []

print(f"Auditing {len(characters)} characters...\n")

for char in characters:
    codepoint = f"U+{ord(char):04X}"
    glyph_name = cmap.get(ord(char))

    if glyph_name is None:
        missing.append((char, codepoint))
        print(f"MISSING: {char!r} ({codepoint})")
        continue

    output_file = OUTPUT_DIR / f"{codepoint}.png"

    if output_file.exists():
        output_file.unlink()

    result = subprocess.run([
        sys.executable,
        "main.py",
        "--font", str(FONT_PATH),
        "--char", char,
        "--output", str(output_file)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        failed.append((char, codepoint, result.stderr.strip()))
        print(f"FAILED: {char!r} ({codepoint})")
    elif output_file.exists():
        passed.append((char, codepoint, glyph_name))
        print(f"PASS: {char!r} -> {glyph_name}")
    else:
        failed.append((char, codepoint, "No output image generated"))
        print(f"NO OUTLINE: {char!r} ({codepoint})")

font.close()

print("\n========== AUDIT SUMMARY ==========")
print(f"Expected characters: {len(characters)}")
print(f"Successfully rendered: {len(passed)}")
print(f"Missing from font: {len(missing)}")
print(f"Rendering failures: {len(failed)}")

if missing:
    print("\nMissing characters:")
    for item in missing:
        print(item)

if failed:
    print("\nFailed characters:")
    for item in failed:
        print(item)