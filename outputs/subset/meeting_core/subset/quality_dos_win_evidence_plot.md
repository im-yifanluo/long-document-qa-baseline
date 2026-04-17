# QuALITY DOS-Win Evidence Plot

This plot covers **all 6** QuALITY subset examples where `dos_rag` scored higher than `vanilla_rag`.

- Plot PNG: `quality_dos_win_evidence_plot.png`
- Plot SVG: `quality_dos_win_evidence_plot.svg`
- Existing HTML walkthrough: `quality_dos_win_evidence_map.html`

Legend:
- Green circle: gold evidence chunk in the actual prompt order
- Red X: explicit distractor chunk in the actual prompt order when one was identified
- Blue bar: vanilla prompt span
- Orange bar: DOS prompt span

## 52845_75VB1ISR_1 - 10 hours vs 12 years

- Vanilla gold positions: `[42]`
- DOS gold positions: `[22]`
- Vanilla distractor positions: `[1]`
- DOS distractor positions: `[23]`
- Vanilla: `12 years`
- DOS: `10 hours`
- Gold: `10 hours`
- Note: Explicit gold and explicit distractor phrase both appear in the story.

## 52845_75VB1ISR_3 - Deirdre / shame / child-in-the-room inference

- Vanilla gold positions: `[2, 3, 1, 4]`
- DOS gold positions: `[9, 13, 14, 17]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`
- Vanilla: `He feels that prostitution is morally reprehensible.`
- DOS: `He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.`
- Gold: `He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.`
- Note: Gold evidence is distributed; no single explicit passage distractor phrase found.

## 62139_J05FWZR6_8 - Meaning of "lady-logic"

- Vanilla gold positions: `[27]`
- DOS gold positions: `[63]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`
- Vanilla: `Condescending logic`
- DOS: `Weak logic`
- Gold: `Weak logic`
- Note: Gold evidence comes from the local usage context of the phrase.

## 62139_J05FWZR6_9 - Would have set course for Iris earlier

- Vanilla gold positions: `[3, 21, 40, 16, 20]`
- DOS gold positions: `[20, 24, 56, 62, 63, 76]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`
- Vanilla: `The text doesn't indicate how the Skipper would've acted in a different scenario.`
- DOS: `The Skipper's would have set course for Iris from the beginning.`
- Gold: `The Skipper's would have set course for Iris from the beginning.`
- Note: Gold answer depends on multiple dispersed chunks.

## 63401_ZCP5ZDGL_7 - Autopilot + asleep in bunk

- Vanilla gold positions: `[5, 6]`
- DOS gold positions: `[5, 6]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`
- Vanilla: `Because he was so exhausted from flying nonstop, with only a few hours of sleep on autopilot, that he fell asleep at the controls.`
- DOS: `Because it was on autopilot and it must've encountered complications that he wasn't able to attend to since he was asleep in his bunk.`
- Gold: `Because it was on autopilot and it must've encountered complications that he wasn't able to attend to since he was asleep in his bunk.`
- Note: Gold evidence is explicit and early in both prompts.

## 63523_STSHLFEA_3 - Fire weapons vs eyes cut the night

- Vanilla gold positions: `[5, 1, 2]`
- DOS gold positions: `[19, 22, 54]`
- Vanilla distractor positions: `[4, 6]`
- DOS distractor positions: `[29, 30]`
- Vanilla: `Their eyes cut the night.`
- DOS: `They have the human's fire weapons.`
- Gold: `They have the human's fire weapons.`
- Note: Explicit gold evidence and explicit distractor phrase both appear in the story.
