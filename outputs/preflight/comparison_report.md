# Comparison Report

Run tier: `preflight`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| contract_nli | exact_match | 100.0000 | 100.0000 | +0.0000 |
| narrative_qa | f1 | 100.0000 | 40.0000 | -60.0000 |
| quality | exact_match | 0.0000 | 100.0000 | +100.0000 |
| qasper | f1 | 33.3333 | 33.3333 | +0.0000 |

## Example Previews

### contract_nli

- examples: 1
- disagreements: 0
- any-positive-score: 1

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, dos_rag
- disagreement: False
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- dos_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…

### narrative_qa

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_0

- query: Which character comes from Bangor, Maine?
- references: Miranda Hope.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Miss Miranda Hope
  scored_as: Miranda Hope.
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…
- dos_rag score: 40.0000
  prediction: Miss Miranda Mope
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…

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

### qasper

- examples: 1
- disagreements: 0
- any-positive-score: 1

#### qasper / b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54

- query: which multilingual approaches do they compare with?
- references: BIBREF19, BIBREF20
- best_methods: vanilla_rag, dos_rag
- disagreement: False
- vanilla_rag score: 33.3333
  prediction: multilingual NMT (MNMT) BIBREF19
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…
- dos_rag score: 33.3333
  prediction: multilingual NMT (MNMT) BIBREF19
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…
