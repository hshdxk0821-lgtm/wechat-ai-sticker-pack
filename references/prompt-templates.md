# Image-generation prompt templates

Use these templates only when the user chooses raster image generation. Keep them short and adapt them to the approved character.

## Optional reference-scope note

Use only when references conflict or the user limits their purpose:

```text
Reference scope: Image 1 supplies [FACE/IDENTITY]. Image 2 supplies [CLOTHING/POSE/STYLE]. Do not copy [BACKGROUND/ACCESSORY/UNWANTED FEATURE].
```

Do not create a role table when one sentence or the approved master is sufficient.

## Master character

```text
Create a polished master character for a WeChat sticker album.

Identity: preserve [FACE SHAPE], [HAIR/HEADWEAR], [GLASSES], [AGE IMPRESSION], and [TEMPERAMENT] from the permitted reference scope.
Design: [USER-CHOSEN DEGREE OF STYLIZATION]. Keep the person recognizable rather than generically cute.
Wardrobe and companions: [APPROVED FEATURES].
Framing: face-forward head and upper body, large enough to judge at chat size.
Background: transparent if supported; otherwise one removable flat color.
Constraints: no words, watermark, unrequested brands, invented accessories, duplicate companions, or identity drift.
```

Show this master to the user. Do not proceed to batch generation until it is explicitly approved.

## Static key pose

```text
Use Image 1, the approved master character, as the primary and default character reference. Create one clean WeChat sticker key pose for the meaning “[PHRASE]”; do not render the phrase itself.

Tone and expression: [EXPRESSION].
Semantic action: [GESTURE].
Optional prop: [PROP OR NONE].
Crop and text-safe area: [CROP AND POSITION].
Preserve from the master: identity, apparent age, face, headwear or hair, glasses, clothing, companions, line quality, palette, and proportions.
Constraints: plausible anatomy and grip, no duplicate face or companion, no unintended writing, no watermark.
```

Use older source photos in addition to the master only when the user requests it or a necessary detail is missing from the master.

When all first-pass static poses are ready, stop image generation and present the complete current set before writing any animation prompt. Show a labeled contact sheet plus the full-resolution files. The review set must use the project's current count; if a planned 16-item set was split into 17, show and obtain approval for all 17. Do not treat approval of a subset, the master, or image-upload permission as approval of the complete static set.

## Animation B frame

Use this template first for the approved representative animation prototypes. Do not batch-generate B/M states for the remaining items until the user has reviewed the actual prototype loops and decoded light/dark frames.

```text
Image 1 is the approved static key pose. Image 2, if supplied, is the approved master identity reference. Create one complete animation end state for “[PHRASE]”.

Frame A: [START STATE].
Frame B: [END STATE].
Meaningful change: [ONLY THE SEMANTIC ACTION].
Expression continuity: keep [EYES], [MOUTH], and [FACE] unchanged unless one is explicitly part of the action.
Composition continuity: preserve character proportions, scale, crop, visual center, clothing, palette, and every non-moving region.
Prop continuity, only when an important prop could look replaced across frames: [ONE SHORT SENTENCE OF VISIBLE IDENTITY INVARIANTS]. Lock visible identity, not motion-dependent position, angle, height, or grip.
Render a fully opaque, complete state with no crossfade, blur, ghost, afterimage, duplicate anatomy, random blink, or whole-canvas movement.
```

## Targeted revision

```text
Revise only [OBSERVABLE PROBLEM].
Required change: [ONE CORRECTION].
Keep unchanged: approved identity, expression except when named, clothing, proportions, crop, palette, text-safe area, non-moving regions, and all already-approved details.
```

For an A/B continuity defect, provide both frames and state which frame controls appearance and which controls action.

## Typography and composite

```text
Text (verbatim): “[EXACT PHRASE]”
Typography: [USER-CHOSEN OR CHARACTER-APPROPRIATE FONT, WEIGHT, FILL, AND OUTLINE].
Placement: keep the text readable at final size and free of face, hand, and prop collisions.
Avoid: substituted characters, decorative distortion, muddy multiple outlines, or effects that reduce small-size clarity.
```

Prefer deterministic text rendering after the artwork is approved.
