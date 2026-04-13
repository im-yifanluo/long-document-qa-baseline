# QuALITY DOS-Win Evidence Position Map

This file summarizes the 6 QuALITY subset examples where `dos_rag` beat `vanilla_rag`. Positions below refer to **actual prompt order**, not retrieval rank.

## 52845_75VB1ISR_1: 10 hours vs 12 years

- Vanilla: `12 years`
- DOS: `10 hours`
- Gold: `10 hours`
- Note: Explicit gold and explicit distractor phrase both appear in the story.
- Vanilla gold positions: `[42]`
- DOS gold positions: `[22]`
- Vanilla distractor positions: `[1]`
- DOS distractor positions: `[23]`

## 52845_75VB1ISR_3: Deirdre / shame / child-in-the-room inference

- Vanilla: `He feels that prostitution is morally reprehensible.`
- DOS: `He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.`
- Gold: `He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.`
- Note: Gold evidence is distributed across multiple nearby chunks; no explicit textual support for the vanilla distractor option.
- Vanilla gold positions: `[2, 3, 1, 4]`
- DOS gold positions: `[9, 13, 14, 17]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`

## 62139_J05FWZR6_8: Meaning of "lady-logic"

- Vanilla: `Condescending logic`
- DOS: `Weak logic`
- Gold: `Weak logic`
- Note: Key evidence is the usage context of the phrase; no explicit distractor phrase found in the passage.
- Vanilla gold positions: `[27]`
- DOS gold positions: `[63]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`

## 62139_J05FWZR6_9: Would have set course for Iris earlier

- Vanilla: `The text doesn't indicate how the Skipper would've acted in a different scenario.`
- DOS: `The Skipper's would have set course for Iris from the beginning.`
- Gold: `The Skipper's would have set course for Iris from the beginning.`
- Note: Gold answer depends on multiple dispersed chunks; vanilla distractor is an ambiguity/default answer rather than a quoted phrase.
- Vanilla gold positions: `[3, 21, 40, 16, 20]`
- DOS gold positions: `[20, 24, 56, 62, 63, 76]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`

## 63401_ZCP5ZDGL_7: Autopilot + asleep in bunk

- Vanilla: `Because he was so exhausted from flying nonstop, with only a few hours of sleep on autopilot, that he fell asleep at the controls.`
- DOS: `Because it was on autopilot and it must've encountered complications that he wasn't able to attend to since he was asleep in his bunk.`
- Gold: `Because it was on autopilot and it must've encountered complications that he wasn't able to attend to since he was asleep in his bunk.`
- Note: Gold evidence is explicit and early; vanilla distractor appears to be an overgeneralization from exhaustion rather than an exact passage phrase.
- Vanilla gold positions: `[5, 6]`
- DOS gold positions: `[5, 6]`
- Vanilla distractor positions: `[]`
- DOS distractor positions: `[]`

## 63523_STSHLFEA_3: Fire weapons vs eyes cut the night

- Vanilla: `Their eyes cut the night.`
- DOS: `They have the human's fire weapons.`
- Gold: `They have the human's fire weapons.`
- Note: Explicit gold evidence and explicit distractor phrase both appear in the story.
- Vanilla gold positions: `[5, 1, 2]`
- DOS gold positions: `[19, 22, 54]`
- Vanilla distractor positions: `[4, 6]`
- DOS distractor positions: `[29, 30]`
