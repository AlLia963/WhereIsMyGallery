import os, sys
from pathlib import Path
from PIL import Image

SEARCH_DIR = Path(__file__).parent
RIPPED_DIR = SEARCH_DIR / "_Ripped" / "Texture2D"

if not RIPPED_DIR.is_dir():
    print(f"'_Ripped/Texture2D' not found. Run extract_all.py first.")
    input("Press Enter to exit...")
    sys.exit(1)

# user input
dim_input = input("Enter target size (e.g. 1920x1080): ").strip()
try:
    w_target, h_target = dim_input.replace("X", "x").split("x")
    w_target, h_target = int(w_target), int(h_target)
except:
    print(f"Invalid format '{dim_input}'. Use WxH, e.g. 1920x1080.")
    input("Press Enter to exit...")
    sys.exit(1)

OUT_DIR = SEARCH_DIR / "_Ripped" / "_Filter" / f"{w_target}x{h_target}"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pngs = list(RIPPED_DIR.glob("*.png"))
print(f"Scanning {len(pngs)} images for {w_target}x{h_target}...")

found = 0
for fp in pngs:
    try:
        img = Image.open(fp)
        if img.size == (w_target, h_target):
            out_path = OUT_DIR / fp.name
            img.save(str(out_path))
            found += 1
            print(f"  [{found:04d}] {fp.name}")
        img.close()
    except:
        pass

print()
print("=" * 60)
print(f"Filtered: {found} images at {w_target}x{h_target}")
print(f"Saved to: {OUT_DIR}")
input("Press Enter to exit...")
