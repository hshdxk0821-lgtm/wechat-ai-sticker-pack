#!/usr/bin/env python3
"""Validate deterministic file requirements for a WeChat sticker package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = value.lower().split("x", 1)
        result = int(width), int(height)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError("size must look like WIDTHxHEIGHT") from exc
    if min(result) <= 0:
        raise argparse.ArgumentTypeError("size values must be positive")
    return result


def find_dir(root: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        candidate = root / name
        if candidate.is_dir():
            return candidate
    return None


def matches_id(path: Path, item_id: str) -> bool:
    return path.stem == item_id or path.stem.startswith(f"{item_id}-") or path.stem.startswith(f"{item_id}_")


def inspect_image(path: Path, expected_size: tuple[int, int] | None, formats: set[str], max_bytes: int | None, animated: bool):
    errors, warnings = [], []
    record = {"file": str(path), "bytes": path.stat().st_size}
    try:
        with Image.open(path) as image:
            fmt = (image.format or "").upper()
            frames = getattr(image, "n_frames", 1)
            record.update({"format": fmt, "width": image.width, "height": image.height, "frames": frames})
            if expected_size is not None and image.size != expected_size:
                errors.append(f"{path.name}: expected {expected_size[0]}x{expected_size[1]}, got {image.width}x{image.height}")
            if fmt not in formats:
                errors.append(f"{path.name}: expected {sorted(formats)}, got {fmt or 'unknown'}")
            if max_bytes is not None and path.stat().st_size > max_bytes:
                errors.append(f"{path.name}: {path.stat().st_size} bytes exceeds {max_bytes}")

            durations, disposals, alpha_extrema, decoded_frames = [], [], [], []
            for index in range(frames):
                image.seek(index)
                rgba = image.convert("RGBA")
                decoded_frames.append(rgba.copy())
                alpha_extrema.append(rgba.getchannel("A").getextrema())
                durations.append(image.info.get("duration"))
                disposals.append(getattr(image, "disposal_method", None))

            actual_transparency = all(extrema[0] < 255 for extrema in alpha_extrema)
            record.update({"transparent": actual_transparency, "alpha_extrema": alpha_extrema})
            if not actual_transparency:
                errors.append(f"{path.name}: every sticker frame must contain actual transparent pixels")

            if animated:
                if frames < 2:
                    errors.append(f"{path.name}: animated mode requires at least 2 frames")
                loop = image.info.get("loop")
                record.update({"loop": loop, "durations_ms": durations, "disposals": disposals})
                if loop != 0:
                    errors.append(f"{path.name}: GIF must loop permanently (loop=0), got {loop!r}")
                if any(value is None or value <= 0 for value in durations):
                    errors.append(f"{path.name}: every frame must have a positive duration")
                if any(value in {None, 0, 1} for value in disposals[1:]):
                    warnings.append(f"{path.name}: some frames may not clear prior content; inspect decoded frames")
                if frames >= 2 and all(ImageChops.difference(decoded_frames[0], frame).getbbox() is None for frame in decoded_frames[1:]):
                    errors.append(f"{path.name}: animation frames decode as identical")
    except Exception as exc:
        errors.append(f"{path.name}: cannot read image ({exc})")
    return errors, warnings, record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    parser.add_argument("--mode", choices=("animated", "static"), default="animated")
    parser.add_argument("--expected-count", type=int, default=24, help="Expected number of stickers (default: 24; override for an explicitly requested count)")
    parser.add_argument("--only-id", help="Validate one rebuilt item before the required full-pack validation")
    parser.add_argument("--main-size", type=parse_size)
    parser.add_argument("--thumb-size", type=parse_size)
    parser.add_argument("--cover-size", type=parse_size)
    parser.add_argument("--icon-size", type=parse_size)
    parser.add_argument("--banner-size", type=parse_size)
    parser.add_argument("--max-main-kb", type=int)
    parser.add_argument("--max-thumb-kb", type=int)
    parser.add_argument("--max-support-kb", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.expected_count is not None and args.expected_count <= 0:
        parser.error("--expected-count must be positive")

    root = args.pack.resolve()
    errors, warnings, records = [], [], []
    main_dir = find_dir(root, ("main", "main-240"))
    thumb_dir = find_dir(root, ("thumbnails", "thumbs", "thumb-120"))
    support_dir = root / "support"
    if not main_dir:
        errors.append("Missing main sticker directory (main; legacy main-240 is also accepted)")
    if not thumb_dir:
        errors.append("Missing thumbnail directory (thumbnails or thumbs; legacy thumb-120 is also accepted)")
    if not args.only_id and not support_dir.is_dir():
        errors.append("Missing support directory")

    ext = ".gif" if args.mode == "animated" else ".png"
    main_files = sorted(main_dir.glob(f"*{ext}")) if main_dir else []
    thumb_files = sorted(thumb_dir.glob("*.png")) if thumb_dir else []
    if args.only_id:
        main_files = [path for path in main_files if matches_id(path, args.only_id)]
        thumb_files = [path for path in thumb_files if matches_id(path, args.only_id)]
        if len(main_files) != 1:
            errors.append(f"Expected one main sticker for id {args.only_id}, found {len(main_files)}")
        if len(thumb_files) != 1:
            errors.append(f"Expected one thumbnail for id {args.only_id}, found {len(thumb_files)}")
    else:
        if args.expected_count is not None and len(main_files) != args.expected_count:
            errors.append(f"Expected {args.expected_count} main stickers, found {len(main_files)}")
        if args.expected_count is not None and len(thumb_files) != args.expected_count:
            errors.append(f"Expected {args.expected_count} thumbnails, found {len(thumb_files)}")

    for path in main_files:
        expected_formats = {"GIF"} if args.mode == "animated" else {"PNG"}
        max_bytes = args.max_main_kb * 1024 if args.max_main_kb is not None else None
        e, w, r = inspect_image(path, args.main_size, expected_formats, max_bytes, args.mode == "animated")
        errors.extend(e); warnings.extend(w); records.append(r)
    for path in thumb_files:
        max_bytes = args.max_thumb_kb * 1024 if args.max_thumb_kb is not None else None
        e, w, r = inspect_image(path, args.thumb_size, {"PNG"}, max_bytes, False)
        errors.extend(e); warnings.extend(w); records.append(r)
    if main_files and thumb_files and [p.stem for p in main_files] != [p.stem for p in thumb_files]:
        errors.append("Main sticker and thumbnail basenames/order do not match")

    if not args.only_id and support_dir.is_dir():
        support_assets = (
            (("cover.png", "cover-240.png"), args.cover_size),
            (("chat-icon.png", "chat-icon-50.png"), args.icon_size),
        )
        for names, size in support_assets:
            path = next((support_dir / name for name in names if (support_dir / name).is_file()), None)
            if path is None:
                errors.append(f"Missing support file; accepted names: {', '.join(names)}")
                continue
            max_bytes = args.max_support_kb * 1024 if args.max_support_kb is not None else None
            e, w, r = inspect_image(path, size, {"PNG"}, max_bytes, False)
            errors.extend(e); warnings.extend(w); records.append(r)
        banners = sorted(set(support_dir.glob("detail-banner.*")) | set(support_dir.glob("detail-banner-*")))
        if not banners:
            errors.append("Missing detail banner in support directory")
        else:
            banner = banners[0]
            try:
                with Image.open(banner) as image:
                    records.append({"file": str(banner), "format": image.format, "width": image.width, "height": image.height, "bytes": banner.stat().st_size})
                    if args.banner_size and image.size != args.banner_size:
                        errors.append(f"{banner.name}: expected {args.banner_size[0]}x{args.banner_size[1]}, got {image.width}x{image.height}")
                    if args.max_support_kb is not None and banner.stat().st_size > args.max_support_kb * 1024:
                        errors.append(f"{banner.name}: file exceeds configured support limit")
            except Exception as exc:
                errors.append(f"{banner.name}: cannot read image ({exc})")

    report = {"pack": str(root), "mode": args.mode, "expected_count": args.expected_count, "only_id": args.only_id, "ok": not errors, "errors": errors, "warnings": warnings, "files": records}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("PASS" if not errors else "FAIL")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARN: {message}")
        print(f"Checked {len(records)} files")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
