#!/usr/bin/env python3
"""Decode animated stickers into light and dark frame-review sheets."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


BACKGROUNDS = {
    "light": (244, 246, 247),
    "dark": (31, 35, 39),
}


def find_main_dir(root: Path) -> Path:
    for name in ("main", "main-240"):
        candidate = root / name
        if candidate.is_dir():
            return candidate
    raise SystemExit("Missing main sticker directory (main; legacy main-240 is also accepted)")


def matches_id(path: Path, item_id: str) -> bool:
    return path.stem == item_id or path.stem.startswith(f"{item_id}-") or path.stem.startswith(f"{item_id}_")


def decode(path: Path) -> tuple[list[Image.Image], list[int | None]]:
    frames, durations = [], []
    with Image.open(path) as image:
        for index in range(getattr(image, "n_frames", 1)):
            image.seek(index)
            frames.append(image.convert("RGBA").copy())
            durations.append(image.info.get("duration"))
    return frames, durations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    parser.add_argument("--id", help="Render only one item id")
    parser.add_argument("--cell-size", type=int, default=120)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    if args.cell_size < 48:
        parser.error("--cell-size must be at least 48")

    root = args.pack.resolve()
    files = sorted(find_main_dir(root).glob("*.gif"))
    if args.id:
        files = [path for path in files if matches_id(path, args.id)]
    if not files:
        raise SystemExit("No matching GIF stickers found")

    decoded = [(path, *decode(path)) for path in files]
    max_frames = max(len(frames) for _, frames, _ in decoded)
    cell = args.cell_size
    label_width = max(150, cell)
    row_height = cell + 24
    width = label_width + max_frames * cell
    height = len(decoded) * row_height
    output_dir = (args.out_dir or root / "preview").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()

    prefix = f"{args.id}-animation-frames" if args.id else "animation-frames"
    for theme, color in BACKGROUNDS.items():
        sheet = Image.new("RGB", (width, height), color)
        draw = ImageDraw.Draw(sheet)
        foreground = (25, 28, 31) if theme == "light" else (240, 243, 245)
        for row, (path, frames, durations) in enumerate(decoded):
            top = row * row_height
            draw.text((8, top + 8), path.stem, fill=foreground, font=font)
            draw.text((8, top + 26), "/".join("?" if value is None else str(value) for value in durations) + " ms", fill=foreground, font=font)
            for column, frame in enumerate(frames):
                preview = ImageOps.contain(frame, (cell, cell), Image.Resampling.LANCZOS)
                background = Image.new("RGBA", (cell, cell), (*color, 255))
                x = (cell - preview.width) // 2
                y = (cell - preview.height) // 2
                background.alpha_composite(preview, (x, y))
                sheet.paste(background.convert("RGB"), (label_width + column * cell, top))
        output = output_dir / f"{prefix}-{theme}.png"
        sheet.save(output, optimize=True)
        print(f"saved={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
