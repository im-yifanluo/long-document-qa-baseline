# Comparison Report

Run tier: `preflight`

## Score Summary

| Task | Metric | read_agent_parallel | read_agent_sequential | read_agent_sequential_minus_read_agent_parallel |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 4.7543 | 10.0448 | +5.2905 |
| narrative_qa | f1 | 40.0000 | 40.0000 | +0.0000 |
| quality | exact_match | 100.0000 | 100.0000 | +0.0000 |

## Example Previews

### qmsum

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: read_agent_sequential
- disagreement: True
- read_agent_parallel score: 4.7543
  prediction: Based on the provided context, the following points were agreed upon regarding sample transcripts: 1. Jose was suggested to mark speaker overlaps for 45 minutes to provide 300 examples for comparison with Adam's automatic method. 2. There was a discussion about using close-talking mikes to infer speech on-off points, which could help speed up the process of marking events. 3. Grad G mentioned hav…
  top_chunk: rank=1 score=n/a Professor E: I probably been affect No , I th I think I 've been affected by too many conversations where we were talking about lawyers and talking about {disfmarker} and concerns about " oh gee is somebody going to say something bad ? " a…
- read_agent_sequential score: 10.0448
  prediction: Based on the provided context, the team agreed to use the transcribed data by Jane as a reference but not to focus on the transcribed words. Jane marked talker changes but did not include temporal marks for overlapping speech zones. The team discussed the possibility of PhD D comparing his marks with Jane's to correct errors and improve accuracy, but they also considered that this process could b…
  top_chunk: rank=1 score=n/a Professor E: Yeah , well , there 's that . But I {disfmarker} I mean I think also to some extent it 's just educating the Human Subjects people , in a way , because there 's {disfmarker} If uh {disfmarker} You know , there 's court transcr…

### narrative_qa

- examples: 1
- disagreements: 0
- any-positive-score: 1

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_0

- query: Which character comes from Bangor, Maine?
- references: Miranda Hope.
- best_methods: read_agent_parallel, read_agent_sequential
- disagreement: False
- read_agent_parallel score: 40.0000
  prediction: Miss Miranda Mope
  top_chunk: rank=1 score=n/a Transcribed from the 1887 Macmillan and Co. edition by David Price, email ccx074@coventry.ac.uk. Proofing by Andy McLauchan and David Stapleton. A BUNDLE OF LETTERS by Henry James CHAPTER I FROM MISS MIRANDA MOPE, IN PARIS, TO MRS. ABRAHAM…
- read_agent_sequential score: 40.0000
  prediction: Miss Miranda Mope
  top_chunk: rank=1 score=n/a Transcribed from the 1887 Macmillan and Co. edition by David Price, email ccx074@coventry.ac.uk. Proofing by Andy McLauchan and David Stapleton. A BUNDLE OF LETTERS by Henry James CHAPTER I FROM MISS MIRANDA MOPE, IN PARIS, TO MRS. ABRAHAM…

### quality

- examples: 1
- disagreements: 0
- any-positive-score: 1

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: read_agent_parallel, read_agent_sequential
- disagreement: False
- read_agent_parallel score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=n/a She laughed. "I am here because I live here," she said. He tried to assimilate the information, but could not. Perceiving his difficulty, the girl went on, "My parents indentured themselves to the Great Starway Cartel and were assigned to…
- read_agent_sequential score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=n/a Presently the girl returned, and not long afterward the cloying scent of native incense crept beneath the arras and permeated the anteroom. She sat sideways on the mat this time, and he caught her face in profile. There was a suggestion of…
