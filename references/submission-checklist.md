# Export, animation review, and submission checklist

Platform fields and limits change. Treat dimensions and byte limits from prior projects or tutorials as working defaults only. Before final export, record the values shown by the current WeChat submission interface and configure the validator accordingly.

## Project specification

Record at least:

| Field | Project value |
|---|---|
| Pack type | static or animated |
| Main sticker count | current accepted count |
| Main format and dimensions | current submission value |
| Thumbnail format and dimensions | current submission value |
| Main and thumbnail byte limits | current submission value |
| Cover and chat-icon requirements | current submission value |
| Detail-banner requirements | current submission value |
| Specification checked on | date |

Do not present tutorial frame counts, colors, timings, or compressed file sizes as platform rules.

## Human approval record

For a new identity-based animated pack, record the artifact version or directory and the user's explicit decision at each gate. Permission to upload or generate references is not artwork approval.

| Gate | Evidence to show | Required before |
|---|---|---|
| Master character | Full review image and approximate chat-size view | Any derivative pose generation |
| Complete static set | Labeled contact sheet plus individual full-resolution poses for the current project count | Any M/B frames, GIFs, thumbnails, covers, or submission assets |
| Animation prototype | Actual loops and decoded light/dark frame strips for representative high-risk items | Batch animation of the remaining set |
| Final pack | All actual loops, decoded light/dark review, PNG-vs-GIF quality comparison, and file-validation report | Calling the pack approved or performing submission |

An intermediate small-group review is useful but does not satisfy the complete static-set gate. If the item count changes, refresh the full contact sheet and approval scope before animation.

## Suggested package layout

```text
sticker-pack/
|-- main/
|-- thumbnails/
|-- support/
|   |-- cover.png
|   |-- chat-icon.png
|   `-- detail-banner.png
|-- preview/
|   |-- contact-sheet-light.png
|   |-- contact-sheet-dark.png
|   |-- animation-frames-light.png
|   `-- animation-frames-dark.png
|-- source/
|-- manifest.json
`-- metadata.md
```

Folder names may follow the current project specification. Use matching stable ids for main stickers and thumbnails.

## Background extraction

- Prefer genuine alpha or a removable flat background.
- For color-based extraction, remove only background-connected pixels; do not globally delete a color that may occur inside the character.
- Use a narrow color tolerance around near-white backgrounds when pale props, eye whites, steam, or light clothing exist.
- Inspect the alpha result over both light and dark backgrounds before resizing and again after final encoding.
- Reject unexpected transparent holes, clipped outlines, opaque halos, or changed prop colors.

## Visual review

- [ ] The master-character version was explicitly approved before derivatives were generated.
- [ ] The complete static key-pose set for the current count was explicitly approved before animation began.
- [ ] Character matches the approved master across the set.
- [ ] Exact phrase is readable at actual display size.
- [ ] Gesture communicates the meaning and feels socially natural.
- [ ] Hands, overlaps, companions, and props are plausible.
- [ ] Text does not collide with the face, hands, or props.
- [ ] Composition remains legible on light and dark chat backgrounds.
- [ ] Typography and palette reflect the current character rather than a previous example pack.

## Decoded animation review

Run:

```powershell
python scripts/render_animation_review.py path/to/sticker-pack
```

For one revised item:

```powershell
python scripts/render_animation_review.py path/to/sticker-pack --id sticker-01
```

Inspect the generated light and dark frame sheets.

- [ ] Each decoded frame is a complete clean state.
- [ ] Only intended action regions change; eyes, mouth, proportions, crop, and other regions remain stable unless intentionally animated.
- [ ] Props retain their count and important visible appearance.
- [ ] No whole-canvas bobbing, crossfade, ghost, residual pixels, palette artifacts, or alpha holes.
- [ ] Tempo and hold time match the meaning.
- [ ] The final loop is comfortable in a real chat view.
- [ ] The actual loop, not only a frame table, has been shown to the user at chat size.
- [ ] Each final GIF has been compared with its approved full-color PNG key pose for face shape, eyes, lips, skin tone, white clothing, and palette loss.

## Targeted revision

1. Preserve the approved source.
2. Save the corrected source as a new revision.
3. Rebuild only the affected id when the project builder supports it, for example `build_pack.py --id sticker-01`.
4. Render and inspect that id's decoded light/dark frame sheets.
5. Run the full validator without an id filter.

## Deterministic validation

Pass the current project limits explicitly when they differ from the defaults:

```powershell
python scripts/validate_sticker_pack.py path/to/sticker-pack --mode animated --expected-count <CURRENT_COUNT> --main-size <WIDTHxHEIGHT> --thumb-size <WIDTHxHEIGHT>
```

Use `--only-id sticker-01` for a fast check immediately after rebuilding one item, then run the full command before delivery. Validation checks file facts and basic decoded-frame facts; it cannot decide resemblance, taste, gesture quality, or whether a small prop variation is acceptable.

## Submission review

- [ ] Required main, thumbnail, cover, icon, banner, and metadata assets are complete.
- [ ] Current submission limits were checked and recorded with a date.
- [ ] The submitter owns or has permission for the artwork, likeness, fonts, props, and marks.
- [ ] Any required identity or portrait-right evidence is ready.
- [ ] Review notifications and post-approval listing or scheduling are confirmed in the platform dashboard.
