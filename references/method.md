# General method for a recognizable sticker pack

## 1. Let the user choose the artwork method

The character may be created with reference-image generation, manual illustration, vector art, 3D rendering, or a mixed workflow. The method is a product choice, not a universal rule.

When the user has not chosen, recommend reference-image generation for photo-based or character-based derivative sets because it usually produces a usable first version faster and makes pose variation easier. Explain the tradeoff: it still needs identity control and per-image inspection. Do not replace the user's chosen method.

Whatever method is selected, deliver the master and all generated states as native transparent RGBA PNGs. Select a generation model that supports native transparent output and explicitly request it in each image call. Use deterministic tools for exact typography, resizing, encoding, contact sheets, and validation.

## 2. The approved master is the main control point

Create one native transparent master character before producing volume. It should establish the face, apparent age, hair or headwear, glasses, signature clothing, accessories, companion characters, illustration language, palette, and default crop.

Review the master at both useful full size and approximate chat size for these outcomes:

1. It looks like the intended person or character.
2. It reflects how that subject should normally appear.
3. The chosen degree of cuteness or stylization does not erase identity.
4. The face and expression remain readable at chat size.

The user must explicitly approve the master. Do not batch-generate derivatives before that approval. Version the approved master and record a compact list of invariant traits, flexible traits, and forbidden drift.

Reference-upload permission or a general instruction to generate images does not approve the resulting master. Approval must refer to the visible master or clearly instruct the workflow to continue from that version.

After approval, derivative generation should normally use the master rather than repeatedly mixing the original photos. This reduces conflicting signals and keeps the set coherent.

## 3. Use references flexibly but honor scope

Reference images do not need a formal role table. Interpret them from the user's request and the visible evidence. Even when references conflict, one short scope note is normally enough.

Record a short usage note only when:

- the user limits a reference to one feature, such as face shape only;
- two references conflict in clothing, age impression, style, or identity;
- a later generation step could accidentally copy an unwanted background, pose, or accessory.

When a restriction exists, preserve it in the master-character prompt. Once the master is approved, it becomes the primary reference for the set.

## 4. Select phrases and design responses

Start with phrases the user actually uses. Fill missing conversational roles only when helpful: acknowledgement, affirmation, interaction, emotion, daily state, encouragement, and farewell.

Plan 24 phrases and key poses by default unless the user explicitly requests another count. For each phrase, define how the character would respond in a real conversation. Specify the facial expression, meaningful gesture, optional prop, crop, text-safe area, A/B action, and tempo. The action should still make sense if the text is temporarily hidden.

Choose one typography style for the pack: font, weight, fill, outline, placement, and phrase-length sizing rule. Keep this style during local text repairs rather than changing a single sticker's text colors or font independently.

Small chat canvases favor head-and-upper-body framing. Use a larger crop only when hands, a prop, or body posture carries the meaning.

## 5. Approve the complete static key-pose set before animating

Check every key pose individually. Look for identity drift, awkward social gestures, random eye closure, changed clothing, duplicate companions, malformed fingers, merged hands and props, and details that disappear after downscaling.

For a large set, inspect small groups during production. Group review catches progressive drift before it affects the whole pack, but it does not replace individual inspection or the complete-set approval gate.

When the first full static set is ready:

1. Use 24 as the expected count unless the user explicitly requests another count; keep the storyboard, source set, exported set, previews, and validator aligned.
2. Show a labeled contact sheet for set-level consistency and provide the individual full-resolution poses for face, hand, and prop inspection.
3. Record the exact version or directory shown to the user.
4. Wait for explicit approval of that complete static set before generating any M/B animation frames, GIFs, thumbnails, covers, or submission files.

The review should cover identity and age impression, face shape and feature spacing, stylization level, expression semantics, hands and anatomy, clothing and accessories, prop identity, crop and safe margins, text-safe space, and color balance. Approval of the master alone does not approve derivative poses.

## 6. Animate semantic changes and lock everything else

Before animating the entire set, make a representative prototype group, normally 3–4 items selected by risk: one face-led expression, one hand-led action, one large-pose or full-body item when present, and one prop-led item when present. Show the actual loops and decoded light/dark frame strips. Expand the animation method only after the user approves facial stability, intended motion, timing, transparency, and encoded color quality.

Default to two complete A/B states. Before prototypes, offer an action-based multi-state option: A/M/B for a simple transition or A/M1/M2/B and additional states for a larger gesture or prop movement. Check the current WeChat dimensions, byte limit, looping requirements, and any published animation restrictions before planning the sequence. Do not invent fixed frame-count or frame-rate platform limits.

Record unique state count, playback order, and each frame's duration separately. For example, an approved A/M/B transition can loop A/M/B/M with longer endpoint holds. More states serve motion continuity and amplitude; they do not require shorter holds or faster playback.

Generate every state as a complete native transparent RGBA PNG using the same item's approved transparent key pose and the approved transparent master as references. The intended action may change the head, hand, mouth, shoulders, posture, or prop. Eyes, mouth, facial proportions, character scale, crop, and other regions remain stable unless explicitly named as part of that action.

Only when an important prop would visibly seem to become a different object between A/B frames, write one compact continuity note rather than a large schema. Include only identity-defining attributes whose change would be distracting, for example:

```text
Prop continuity: preserve [COUNT], [COLOR OR MATERIAL], [DISTINCTIVE MARK], and [CONTENTS] in A and B; allow the angle, position, or grip to change with the action.
```

Do not add this note when there is no important prop. Lock visible identity, not motion-dependent height, angle, position, or grip. Judge minor variation at the final configured display size: accept differences that do not affect the reading, and revise visible object replacement locally.

Do not manufacture animation by scaling or translating the finished canvas. Do not crossfade complete character frames. Encode clean states with correct disposal so each frame replaces the previous state without ghosts.

## 7. Use native transparent sources and review encoding

The master, static key poses, and all animation states must arrive as native transparent RGBA PNGs. Generated outputs with an opaque background or a painted checkerboard are rejected and regenerated as transparent images. If the generation model lacks native transparent output, report the capability limitation before production. Do not substitute a background-extraction workflow.

The source image looking correct is not enough. Decode the final GIF, place every frame on both light and dark backgrounds, and inspect the result. Compare the decoded GIF next to the full-color PNG or other master frame at the intended chat size. This reveals alpha holes, palette-index mistakes, residual frames, outline loss, facial deformation, palette loss, yellow or other white-balance drift, and unexpected color changes.

For GIF, explicitly inspect eyes, lips, skin gradients, and pale clothing. These areas often lose quality because one transparent palette index leaves at most 255 visible colors. If the decoded GIF is materially worse than the approved PNG, revise palette allocation, dithering, artwork shading complexity, or animation format before presenting it as final; do not treat successful decoding as visual approval.

## 8. Revise locally and preserve approved work

When one item has a defect:

1. Identify whether the fault is in source generation, native transparency, typography, scaling, palette conversion, or animation encoding.
2. Change only that cause.
3. Save a versioned source replacement rather than destroying approved source art.
4. Rebuild only the affected sticker and its thumbnail when the build workflow supports an item id such as `--id sticker-01`.
5. Inspect the decoded frames for that item.
6. Run the full-pack validator to ensure the package remains complete.

Human judgment controls resemblance and taste; scripts control repeatable file facts.
