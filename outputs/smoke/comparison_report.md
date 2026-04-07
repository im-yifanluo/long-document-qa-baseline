# Comparison Report

Run tier: `smoke`

## Score Summary

| Task | Metric | dos_rag |
| --- | --- | --- |
| qmsum | rouge | 0.0000 |

## Example Previews

### qmsum

- examples: 2
- disagreements: 0
- any-positive-score: 0

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: dos_rag
- disagreement: False
- dos_rag score: 0.0000
  prediction: 

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: dos_rag
- disagreement: False
- dos_rag score: 0.0000
  prediction:
