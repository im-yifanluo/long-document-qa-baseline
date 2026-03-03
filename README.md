# SCROLLS RAG Baseline Benchmark

A flat-RAG baseline system evaluated on the [SCROLLS](https://www.scrolls-benchmark.com/) long-document benchmark.

## Architecture

```
Document ─► TokenChunker (512 tok, 64 overlap)
         ─► BGE-large-en-v1.5 embedding
         ─► FAISS flat-IP index
         ─► Top-40 retrieval → context assembly (≤ 16 000 tokens)
         ─► Qwen 2.5-32B-Instruct generation
         ─► ROUGE / F1 / Exact-Match evaluation
```

| Parameter        | Value                   |
|------------------|-------------------------|
| Embedding model  | `BAAI/bge-large-en-v1.5`|
| LLM              | Qwen 2.5-32B-Instruct (local vLLM) |
| Chunk size       | 512 tokens              |
| Chunk overlap    | 64 tokens               |
| Top-k            | 40                      |
| Context budget   | 16 000 tokens           |

## SCROLLS Tasks & Metrics

| Task           | Type                  | Metric                      |
|----------------|-----------------------|-----------------------------|
| gov_report     | Summarisation         | ROUGE-1/2/L (geo mean)      |
| summ_screen_fd | Summarisation         | ROUGE-1/2/L (geo mean)      |
| qmsum          | Query summarisation   | ROUGE-1/2/L (geo mean)      |
| squality       | Query summarisation   | ROUGE-1/2/L (geo mean)      |
| qasper         | Question answering    | Token-level F1              |
| narrative_qa   | Question answering    | Token-level F1              |
| quality        | Multiple choice       | Exact match (accuracy)      |
| contract_nli   | NLI classification    | Exact match (accuracy)      |

---

## Quick start (SSH server workflow)

### 1. Setup

```bash
# SSH into the server
ssh user@server

# Clone / navigate to the project
cd /path/to/baseline_benchmark

# One-time setup (creates venv, installs deps)
bash setup.sh
source venv/bin/activate
```

### 2. Verify the generator works

Test that the LLM loads and responds before committing to a full benchmark run.

```bash
# Single prompt
python test_generator.py \
    --llm-model Qwen/Qwen2.5-32B-Instruct \
    --prompt "What is the capital of France?"

# Interactive REPL
python test_generator.py \
    --llm-model Qwen/Qwen2.5-32B-Instruct

# Custom system prompt
python test_generator.py \
    --llm-model Qwen/Qwen2.5-32B-Instruct \
    --system-prompt "You are a helpful research assistant." \
    --prompt "Explain RAG in one paragraph."
```

### 3. Smoke test (end-to-end validation)

Runs 2 examples from `qasper` + `gov_report` through the full pipeline.

```bash
python smoke_test.py --llm-model Qwen/Qwen2.5-32B-Instruct
```

Override tasks / sample count:

```bash
python smoke_test.py \
    --llm-model Qwen/Qwen2.5-32B-Instruct \
    --tasks qasper narrative_qa quality contract_nli \
    --num-samples 3
```

### 4. Full benchmark

```bash
# All 8 tasks, full validation set
python run_benchmark.py --llm-model Qwen/Qwen2.5-32B-Instruct

# Specific tasks
python run_benchmark.py \
    --llm-model Qwen/Qwen2.5-32B-Instruct \
    --tasks qasper narrative_qa quality

# Limit samples (for quick iteration)
python run_benchmark.py \
    --llm-model Qwen/Qwen2.5-32B-Instruct \
    --max-samples 50
```

---

## CLI reference

### `run_benchmark.py`

| Flag | Default | Description |
|------|---------|-------------|
| `--tasks` | all 8 | SCROLLS tasks to evaluate |
| `--split` | `validation` | Dataset split |
| `--max-samples` | `-1` (all) | Cap examples per task |
| `--llm-model` | `Qwen/Qwen2.5-32B-Instruct` | LLM model ID or path |
| `--embedding-model` | `BAAI/bge-large-en-v1.5` | Embedding model |
| `--chunk-size` | `512` | Tokens per chunk |
| `--chunk-overlap` | `64` | Token overlap between chunks |
| `--top-k` | `40` | Chunks to retrieve |
| `--context-budget` | `16000` | Max context tokens |
| `--max-new-tokens` | `1024` | Max generation tokens |
| `--temperature` | `0.0` | Sampling temperature |
| `--embedding-device` | `cuda` | Device for embedding model |
| `--gpu-memory-utilization` | `0.90` | vLLM GPU memory fraction |
| `--tensor-parallel-size` | `1` | GPUs for tensor parallelism |
| `--output-dir` | `outputs` | Where to save results |
| `--no-save-raw` | flag | Disable per-example JSONL output |
| `--log-level` | `INFO` | Logging verbosity |

### `smoke_test.py`

Same model/hardware flags as above, plus:

| Flag | Default | Description |
|------|---------|-------------|
| `--num-samples` | `2` | Examples per task |
| `--tasks` | `qasper gov_report` | Tasks to smoke-test |

### `test_generator.py`

| Flag | Default | Description |
|------|---------|-------------|
| `--llm-model` | (required) | Model to load |
| `--prompt` | (none) | Single user prompt; omit for interactive mode |
| `--system-prompt` | `You are a helpful assistant.` | Custom system prompt |
| `--max-new-tokens` | `512` | Max generation length |
| `--temperature` | `0.0` | Sampling temperature |

---

## Output structure

```
outputs/
├── benchmark_report.json          # Overall scores + config
├── benchmark.log                  # Full log
├── gov_report/
│   ├── results.jsonl              # Per-example raw outputs
│   └── summary.json               # Task-level metrics
├── qasper/
│   ├── results.jsonl
│   └── summary.json
└── …                              # One folder per task
```

### Raw output format (`results.jsonl`)

Each line is a JSON object:

```json
{
  "id": "example_id",
  "task": "qasper",
  "query": "What method was used for …?",
  "prediction": "The authors used …",
  "references": ["They employed …"],
  "num_chunks": 87,
  "num_retrieved": 40,
  "num_context_chunks": 32,
  "context_tokens": 15823,
  "system_prompt": "You are a helpful assistant …",
  "user_prompt": "Context:\n…\n\nQuestion: …"
}
```

This lets you inspect exactly what the model saw (full prompt) and produced.

---

## Resume support

If a run is interrupted, simply re-run the same command.  The pipeline
detects existing `results.jsonl` files and skips already-processed examples.

---

## Project structure

```
baseline_benchmark/
├── config.py            # Task metadata, prompt templates, RAGConfig dataclass
├── data_loader.py       # SCROLLS dataset loading & input parsing
├── chunker.py           # Token-level document chunking
├── embedder.py          # BGE-large-en-v1.5 sentence-transformers wrapper
├── retriever.py         # FAISS flat-IP index per document
├── generator.py         # vLLM local offline generation
├── rag_pipeline.py      # Full RAG orchestration + evaluation
├── metrics.py           # ROUGE, F1, exact-match scorers
├── run_benchmark.py     # Main CLI
├── smoke_test.py        # Quick end-to-end validation
├── test_generator.py    # Test LLM with custom prompts
├── requirements.txt     # Python dependencies
├── setup.sh             # One-command environment setup
└── README.md            # This file
```
