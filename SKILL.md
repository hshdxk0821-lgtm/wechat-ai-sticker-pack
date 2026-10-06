---
name: wechat-ai-sticker-pack
description: Create or revise a recognizable WeChat sticker album from photos or an established character, with staged human approval of the master, complete static key-pose set, animation samples, and final pack, plus export and submission QA. Use for 微信表情包、真人转Q版表情、动态表情、表情专辑或微信投稿素材。
---

# WeChat Sticker Pack

Create a sticker album that remains recognizable and readable in real chat, and deliver a complete, reviewable submission package.

## Production defaults

- Produce 24 stickers by default. Use the same count for the storyboard, complete static set, complete animated set, previews, and validation; change it only when the user explicitly requests another count.
- Default animation to two complete A/B states. Before the animation prototypes, offer an action-based multi-state option such as A/M/B or A/M1/M2/B. Plan state count and per-frame durations separately; additional states do not imply faster playback. Check current WeChat limits before selecting the sequence and timing.
- Create the master, static key poses, and every animation state as native transparent RGBA PNGs. Use the approved transparent master and the same item's transparent key pose as references. Require a generation model that supports native transparent output and explicitly request it in every image call. Opaque backgrounds or painted checkerboards are rejected and regenerated; there is no background-extraction fallback. If the available model cannot output native transparency, report that capability limitation before production.
- Use one typography style across the entire pack: font, weight, fill, outline, and placement rules. Local text repairs must preserve this style; fit longer phrases using the same sizing rule.

## Route the task

- Read [references/method.md](references/method.md) before planning the character, phrases, poses, or animation.
- Read [references/prompt-templates.md](references/prompt-templates.md) only when generating or revising raster artwork with an image model.
- Read [references/submission-checklist.md](references/submission-checklist.md) when handling native transparency, encoding animation, exporting, revising a finished item, or preparing submission.
- After export, run `scripts/render_animation_review.py` for animated packs and inspect decoded frames on light and dark backgrounds. Then run `scripts/validate_sticker_pack.py` for file-level checks.

## Mandatory human approval gates

For a new multi-item identity-based pack, stop at each applicable gate and show the named artifacts at a useful review size. An explicit approval such as “可以”“按这版继续” is sufficient; do not demand a formal checklist or repeat decisions the user already made. Permission to upload references, permission to generate images, or approval of an earlier gate is **not** approval of a later artifact.

1. **Master-character gate — before derivative generation.** Show the master at full review size and at approximate chat size. Ask the user to judge resemblance, apparent age, face proportions, stylization level, hair or headwear, clothing, accessories, palette, and default crop. Do not generate the derivative set until the master is explicitly approved.
2. **Complete static-set gate — before any animation-state generation.** Produce the complete first-pass static key-pose set for the current project count, defaulting to 24. Show a labeled contact sheet plus links or files for individual full-resolution poses. Ask the user to judge identity consistency, expression and phrase fit, hand anatomy, props, clothing, crop, text-safe space, and color balance. Small-group checks may catch drift during production, but they do not replace approval of the complete static set. Do not create M/B animation states, GIFs, or submission assets until this full static set is explicitly approved.
3. **Animation-prototype gate — before batch animation.** For a new animated pack, animate a small representative sample that covers the main risks, normally 3–4 items: a face-led expression, a hand-led action, a large pose or full-body item when present, and a prop-led item when present. Show actual looping files and decoded light/dark frame strips. Confirm facial stability, motion meaning, object continuity, timing, transparency, and GIF color quality before expanding the animation method to the rest of the set.
4. **Final-pack gate — before treating the work as finished or submission-ready.** Show all final stickers in an actual looping review page or equivalent playback view, along with decoded frames on light and dark backgrounds. Separately report visual review and deterministic file validation. Wait for final user approval before calling the pack approved, replacing a prior approved version, or proceeding to a submission action.

For a targeted revision, apply only the gates affected by the change: review the changed full-color source or static pose, review that item's real animation when applicable, and revalidate the complete pack. Do not force reapproval of an unchanged master or unchanged static set.

## Workflow

1. Confirm the intended pack type and the user's preferred artwork method. The choice belongs to the user. When no method is specified, explain that reference-image generation is usually faster and more consistent for a large derivative set, recommend it, and let the user decide. Follow an explicit request for hand drawing, vector work, or another method.
2. Inspect references contextually. Respect explicit limits such as “use only the face.” If references conflict or their intended use is ambiguous, resolve the scope with one short note; do not require a formal reference-role table.
3. Create one master character and complete the master-character approval gate. Record only the identity traits that materially affect consistency. **Do not batch-generate derivative stickers until the user explicitly approves this master.**
4. After approval, use the master as the default character reference for derivatives. Return to older source photos only when the user requests it or the approved master cannot supply a necessary detail.
5. Agree on the phrase list for 24 items by default and write a compact storyboard for each item: meaning, expression, semantic action, crop, optional prop, intended A/B change, and tempo. For an approved multi-state option, record the intermediate states, playback sequence, and per-frame durations. Preserve user wording exactly. Default to head-and-upper-body framing; expand only when the action needs it.
6. Produce clean static key poses, then complete the mandatory complete static-set gate for the project's current count. For larger sets, review small groups during production to catch drift, but still show and obtain approval for the complete set before animation.
7. For a new animated pack, offer default A/B animation and an action-based multi-state option, then complete the animation-prototype gate before batch animation. Make each selected state as a complete native transparent RGBA image. Keep eyes, mouth, facial proportions, body scale, color balance, and all non-moving regions stable unless one of them is the intended semantic action. Add one short prop-continuity note only when an important prop would otherwise appear to become a different object across frames; lock its visible identity without preventing motion-dependent changes.
8. Add exact text as a deterministic layer when practical. Choose one typography and color treatment for the pack from the current character and user preference. Preserve that treatment during local text repairs.
9. Export the native transparent artwork against the limits shown by the current WeChat submission interface. Render decoded animation frames on both light and dark backgrounds, inspect them at actual chat size, run deterministic validation, and complete the final-pack approval gate.
10. For a local defect, preserve approved source art, save a versioned replacement, rebuild only the affected sticker and thumbnail when possible, inspect that item's decoded frames, and finally revalidate the complete pack.

## Quality gates

- The approved master remains recognizable across the set; no unrequested identity, age, clothing, or style drift.
- Each action communicates its phrase without depending entirely on text.
- Hands, limbs, overlaps, and props are plausible; there are no duplicate faces, unexplained objects, or fused anatomy.
- Eyes, mouth, proportions, framing, and non-action regions do not change randomly between animation frames.
- When an important prop needs continuity, its count and visually defining appearance remain stable across A/B frames. Allow changes in angle, position, height, or grip that the action requires, and accept minor differences that are not noticeable at the final configured display size.
- Chinese text is exact and readable at the final display size, with sufficient contrast and no collisions.
- Animation uses fully rendered states, loops cleanly, and has no crossfade ghosts, residual pixels, palette artifacts, or whole-canvas motion standing in for acting.
- Native transparent artwork preserves light-colored foreground objects. Dark details remain legible on dark chat backgrounds.
- All requested assets exist and pass the current project specification for count, dimensions, format, transparency, looping, and file size.

File validation is not visual approval. A pack is finished only after the decoded final files—not merely the source art—have been reviewed in chat-like conditions.
