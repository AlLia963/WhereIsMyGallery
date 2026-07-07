# Unity Asset Extractor

Drop this folder into your Unity game directory, double-click `run.bat`, and all art assets (textures, sprites, audio) get extracted automatically. Then `run2nd.bat` to filter by resolution.

## Requirements

- Python 3.10+
- `pip install unitypy Pillow`

## Quick Start

```
1. Copy all files into the game's root folder (where the *_Data folder lives)
2. Double-click run.bat -> waits for full extraction -> _Ripped/Texture2D/
3. Double-click run2nd.bat -> enter e.g. 1920x1080 -> _Ripped/_Filter/1920x1080/
```

## Files

| File | Purpose |
|------|---------|
| `extract_all.py` | Recursively scans all .bundle / .assets files, exports Texture2D, AudioClip, TextAsset |
| `run.bat` | One-click launcher for extract_all.py |
| `extract_filter.py` | Scans _Ripped/Texture2D, copies images matching target WxH into _Ripped/_Filter/WxH/ |
| `run2nd.bat` | One-click launcher for extract_filter.py |

## How It Works

- Recursive glob from script location — no hardcoded paths, works across Unity game
- Supports UnityFS bundles from Unity 5.x to Unity 6

## Limitations

- Encrypted bundles (header != `UnityFS`) won't open — requires reverse engineering the decryption key first
- Non-Unity engines (Ren'Py, Kirikiri, etc.) are not supported
- UnityPy may lag behind bleeding-edge Unity releases by a few weeks

## License

MIT.

## Disclaimer

This tool reads UnityFS-formatted container files for educational and archival purposes. It does not contain, distribute, or host any copyrighted game assets. Users are responsible for complying with applicable game EULAs and local laws. The author assumes no liability for how this tool is used.
