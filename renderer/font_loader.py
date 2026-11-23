"""
FONT LOADER
Purpose:
    Open a TTF/OTF font and find the glyph corresponding to a character.

Algorithm steps:
    1. Open the font with FontTools.
    2. Read the font's character-to-glyph mapping (cmap).
    3. Read unitsPerEm so font coordinates can later be scaled to pixels.
    4. Look up the requested character and retrieve its glyph object.
    5. Provide the glyph set to the flattening pen so composite glyphs can be drawn.

This module locates glyph data. Curve processing is handled by flattening.py.
"""

from fontTools.ttLib import TTFont


class FontLoader:
    def __init__(self, font_path):
        self.font = TTFont(str(font_path))
        self.glyph_set = self.font.getGlyphSet()
        self.character_map = self.font.getBestCmap() or {}

        if "head" not in self.font:
            self.font.close()
            raise ValueError("The font does not contain a 'head' table.")

        self.units_per_em = self.font["head"].unitsPerEm

    def get_glyph(self, character):
        """Return (glyph_name, glyph_object, glyph_set) for one character."""
        if len(character) != 1:
            raise ValueError("Provide exactly one character.")

        glyph_name = self.character_map.get(ord(character))
        if glyph_name is None:
            raise ValueError(f"The font does not contain a glyph for {character!r}.")

        return glyph_name, self.glyph_set[glyph_name], self.glyph_set

    def close(self):
        self.font.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
