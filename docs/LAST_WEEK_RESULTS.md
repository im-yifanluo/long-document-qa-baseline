# Last Week's Benchmark Results

This note answers one question that is easy to get wrong when reading the saved
 reports:

> Is DOS-RAG here basically "feed the original passage" because the context is large?

Short answer:

- No, DOS-RAG is still retrieval-based in this repo.
- But on several SCROLLS subset tasks, the 10k-token budget is large enough that
  retrieval ends up covering almost the whole document.
- In those cases, the benchmark is less about "which chunks were found" and more
  about "what order the model reads nearly the same evidence in."

## How `vanilla_rag` vs `dos_rag` is implemented here

`vanilla_rag`:

1. chunk the document
2. retrieve top chunks by similarity
3. keep adding retrieved chunks until the `context_budget` is full
4. prompt the reader in retrieval-rank order

`dos_rag`:

1. use the official DOS-RAG chunking/retrieval core from `dos-rag-eval`
2. retrieve top chunks under the same `context_budget`
3. restore the selected chunks to original document order
4. prompt the same reader on that reordered context

So the critical benchmark difference is not "retrieval vs no retrieval." It is:

- `vanilla_rag`: relevance order
- `dos_rag`: original document order after retrieval

## What last week's subset results actually show

From `outputs/subset/meeting_core/subset`:

| Task | vanilla_rag | dos_rag | delta |
|---|---:|---:|---:|
| `qmsum` | 16.6505 | 18.2178 | +1.5673 |
| `qasper` | 51.4486 | 54.4233 | +2.9747 |
| `narrative_qa` | 19.5300 | 21.6398 | +2.1098 |
| `quality` | 70.0000 | 78.0000 | +8.0000 |
| `contract_nli` | 72.0000 | 66.0000 | -6.0000 |
| average | 45.9258 | 47.6562 | +1.7304 |

Main pattern:

- DOS helps on `qmsum`, `qasper`, `narrative_qa`, and especially `quality`
- DOS hurts on `contract_nli`

## How much of the document is actually being shown?

Using the saved `results.jsonl` rows from last week's DOS run:

| Task | examples with DOS context >= 95% of document |
|---|---:|
| `qmsum` | 33 / 50 |
| `qasper` | 50 / 50 |
| `narrative_qa` | 0 / 50 |
| `quality` | 50 / 50 |
| `contract_nli` | 50 / 50 |

Implication:

- On `qasper`, `quality`, and `contract_nli`, DOS is often very close to
  "retrieve nearly the whole document, then read it in original order."
- On `qmsum`, that is true for many but not all examples.
- On `narrative_qa`, DOS is still a real sparse-selection method because only a
  minority of the very long source document fits.

## Why this matters scientifically

When the full document fits inside the budget, the comparison is not mainly:

- "Did DOS retrieve better evidence than vanilla?"

It becomes much closer to:

- "What happens if we show nearly the same evidence, but in document order
  instead of retrieval rank?"

That is still a useful result, but it changes the interpretation:

- `quality`: strong evidence that ordering and local discourse continuity help
- `contract_nli`: strong evidence that restoring early boilerplate can bury the
  answer-bearing clause
- `narrative_qa`: more representative of true long-document retrieval because
  ordering matters under real selection pressure

## Example-level intuition from saved runs

### QuALITY: DOS win can look like "near-full-document + better order"

For `52845_75VB1ISR_1`:

- `vanilla_rag`: 76 chunks, presented in scrambled relevance order
- `dos_rag`: 76 chunks, presented as chunk indices `0..75`

So DOS did not simply use a larger budget there. It used almost the same amount
of evidence, but arranged it as a coherent passage.

### ContractNLI: DOS loss can look like "original order restores boilerplate too"

For `7_nda-11`:

- `vanilla_rag`: 78 chunks in relevance order
- `dos_rag`: 76 chunks presented as chunk indices `0..75`

That means DOS effectively reconstructs the front of the contract. If the
answer-bearing clause is not near the front, the restored order can make the
reader wade through boilerplate before reaching the important clause.

## Best interpretation to use in discussion

The cleanest way to describe last week's result is:

- DOS-RAG in this repo is not a pure long-context baseline.
- It is still retrieval-based, but on several SCROLLS subset tasks the 10k-token
  budget is generous enough that the benchmark mostly becomes an ordering test
  over nearly the same evidence.
- That helps explain why DOS looks especially strong on narrative or distractor-
  heavy questions, while it can regress on clause-local legal reasoning.

## Practical next step

If you want a stronger causal claim, the next ablation should be:

1. retrieve the same chunk set as vanilla
2. change only the prompt ordering to document order
3. compare that against both `vanilla_rag` and `dos_rag`

This repo now exposes that ablation directly as `reorder_only_rag`.

That will separate:

- ordering effect
- retrieval-core effect

much more cleanly than the current two-way comparison.
