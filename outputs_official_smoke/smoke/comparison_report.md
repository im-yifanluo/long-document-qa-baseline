# Comparison Report

Run tier: `smoke`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qasper | f1 | 66.6667 | 66.6667 | +0.0000 |
| quality | exact_match | 0.0000 | 50.0000 | +50.0000 |

## Example Previews

### qasper

- examples: 1
- disagreements: 0
- any-positive-score: 1

#### qasper / b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54

- query: which multilingual approaches do they compare with?
- references: multilingual NMT (MNMT) BIBREF19
- best_methods: vanilla_rag, dos_rag
- disagreement: False
- vanilla_rag score: 100.0000
  prediction: multilingual NMT (MNMT) BIBREF19
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…
- dos_rag score: 100.0000
  prediction: multilingual NMT (MNMT) BIBREF19
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…

### quality

- examples: 2
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

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: vanilla_rag, dos_rag
- disagreement: False
- vanilla_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- dos_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
