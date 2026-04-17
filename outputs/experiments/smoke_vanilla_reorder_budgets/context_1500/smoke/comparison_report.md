# Comparison Report

Run tier: `smoke`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| quality | exact_match | 0.0000 | 0.0000 | +0.0000 |
| contract_nli | exact_match | 100.0000 | 100.0000 | +0.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 8.50 | 0.14 | 2.1250 | 0.4706 |
| reorder_only_rag | 3.85 | 0.06 | 0.9625 | 1.0390 |

## Example Previews

### quality

- examples: 2
- disagreements: 0
- any-positive-score: 0

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: False
- vanilla_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- reorder_only_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: False
- vanilla_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- reorder_only_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…

### contract_nli

- examples: 2
- disagreements: 0
- any-positive-score: 2

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: False
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…

#### contract_nli / 3_nda-16

- query: Receiving Party shall destroy or return some Confidential Information upon the termination of Agreement.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: False
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6882 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6882 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
