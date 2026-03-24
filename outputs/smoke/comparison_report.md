# Comparison Report

Run tier: `smoke`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qasper | f1 | 22.2200 | 13.3300 | -8.8900 |
| quality | exact_match | 0.0000 | 100.0000 | +100.0000 |

## Example Previews

### qasper

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### qasper / b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54

- query: which multilingual approaches do they compare with?
- references: BIBREF19, BIBREF20
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 22.2222
  prediction: They compare with multilingual NMT (MNMT) BIBREF19.
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…
- dos_rag score: 13.3333
  prediction: They compare with multilingual NMT (MNMT) BIBREF19 and cross-lingual transfer without pretraining BIBREF16.
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…

### quality

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- dos_rag score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
