import os, sys
from pathlib import Path

SEARCH_DIR = Path(__file__).parent
OUT_DIR = SEARCH_DIR / "_Ripped"

try:
    from UnityPy import Environment
except ImportError:
    print("=" * 60)
    print("UnityPy not installed.")
    print("Run: pip install unitypy")
    print("=" * 60)
    input("Press Enter to exit...")
    sys.exit(1)

bundle_files = []
for p in ["*.bundle", "*.unity3d", "*.assets"]:
    bundle_files.extend(SEARCH_DIR.rglob(p))

skip = {"globalgamemanagers", "resources", "sharedassets0"}
bundle_files = [f for f in bundle_files if f.stem not in skip]

if not bundle_files:
    print("No bundle/asset files found. Put this script next to the *_Data folder.")
    input("Press Enter to exit...")
    sys.exit(1)

print(f"Found {len(bundle_files)} asset files")
print(f"Output: {OUT_DIR}")
print("Extracting...")

stats = {"tex": 0, "audio": 0, "text": 0, "err": 0}

for i, fp in enumerate(bundle_files):
    try:
        rel = fp.relative_to(SEARCH_DIR)
    except:
        rel = fp.name
    print(f"  [{i+1}/{len(bundle_files)}] {rel}", end="", flush=True)
    try:
        env = Environment()
        env.load_file(str(fp))
        count = 0
        for asset in env.assets:
            for obj in asset.objects.values():
                t = obj.type.name if obj.type else "?"
                try:
                    data = obj.read()
                    if t in ("Texture2D", "Sprite"):
                        img = data.image
                        if img is not None:
                            name = getattr(data, 'name', '') or f"tex_{obj.path_id}"
                            safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in str(name)).strip()[:80] or f"u_{obj.path_id}"
                            p = OUT_DIR / "Texture2D" / f"{safe}.png"
                            p.parent.mkdir(parents=True, exist_ok=True)
                            img.save(str(p))
                            stats["tex"] += 1
                            count += 1
                    elif t == "AudioClip":
                        raw = getattr(data, 'm_AudioData', None)
                        if raw:
                            name = getattr(data, 'name', '') or f"audio_{obj.path_id}"
                            safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in str(name)).strip()[:80] or f"u_{obj.path_id}"
                            p = OUT_DIR / "AudioClip" / f"{safe}.wav"
                            p.parent.mkdir(parents=True, exist_ok=True)
                            with open(p, "wb") as f:
                                f.write(raw if isinstance(raw, bytes) else bytes(raw))
                            stats["audio"] += 1
                            count += 1
                    elif t == "TextAsset":
                        script = getattr(data, 'script', None)
                        if script:
                            name = getattr(data, 'name', '') or f"text_{obj.path_id}"
                            safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in str(name)).strip()[:80] or f"u_{obj.path_id}"
                            p = OUT_DIR / "TextAsset" / f"{safe}.txt"
                            p.parent.mkdir(parents=True, exist_ok=True)
                            with open(p, "wb") as f:
                                f.write(script if isinstance(script, bytes) else script.encode('utf-8', errors='replace'))
                            stats["text"] += 1
                            count += 1
                except:
                    pass
        if count:
            print(f"  -> {count} assets")
        else:
            print("  (empty)")
    except Exception as e:
        print(f"  [Err: {type(e).__name__}]")
        stats["err"] += 1

print()
print("=" * 60)
print("Done!")
print(f"  Texture2D : {stats['tex']}")
print(f"  AudioClip : {stats['audio']}")
print(f"  TextAsset : {stats['text']}")
if stats["err"]:
    print(f"  Errors    : {stats['err']}")
print(f"Files saved to: {OUT_DIR}")
input("Press Enter to exit...")
