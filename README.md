# ANANSE SVG Glyph Workspace

This starter package exports the 93 visible glyphs in the current ANANSE font as individual SVG files and creates a contact sheet plus CSV/JSON manifests.

## Important
This is an **export and review workspace**, not a completed Adinkra redesign. It exports the outlines currently present in your TTF. It does not invent symbol geometry or claim that the symbols have been structurally integrated. The approved master concept artwork must be used to trace and integrate each Adinkra symbol before a glyph is marked final.

## Install
```powershell
py -m pip install -r requirements.txt
```

## Run
From the GhanaTypefaceRenderer project folder:
```powershell
py generate_glyphs.py --font fonts/ANANSE-Regular.ttf --output ANANSE_SVG_Output
```

## Output
- `glyphs/U+XXXX.svg`: individual SVGs
- `ANANSE_93_Glyph_Contact_Sheet.png`
- `glyph_manifest.csv`
- `glyph_manifest.json`

## Inventory
93 visible characters: A-Z, a-z, 0-9, Ɛ ɛ Ɔ ɔ, `.,:;!?-()[]`, `+ − × ÷ =`, `' "`, `/ \\`, and `@ # $ % ^ & *`. Space is a spacing character and is not included among the 93 visible outlines.

## Mapping status
Confirmed mappings are listed in `adinkra_geometry.py`. D/E/F are proposed and require your approval. Other mappings remain unassigned until established.

## Next step
Trace symbol paths from the approved ANANSE master concept artwork, then integrate those paths into the actual letter outlines. Do not simply paste symbols inside ordinary letters.
