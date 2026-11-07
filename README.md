# LLM Eval Workbench

**GenAI** · A reproducible regression gate for saved model responses.

## Run locally

Python 3.11+; no third-party packages required. From this directory:

```bash
python main.py demo
python main.py run example.json
python -m unittest discover -s tests -v
```

`example.json` is the input contract and contains only synthetic or fictional data. `core.run(payload)` returns a JSON-serializable result. Invalid inputs produce an error and a nonzero CLI exit code.

## What it implements

- Versioned rubric checks for required phrases, forbidden content, citation format, refusal and JSON-schema-like requirements.
- Per-case pass/fail evidence and aggregate checks, case scores and release threshold.
- Compares baseline and candidate runs to expose regressions.
- Exports structured results suitable for CI; no paid inference is needed.

## Design and limitations

This is a rule-based LLM evaluation harness, not an LLM and not a comprehensive safety evaluator. It evaluates supplied responses; it does not generate them. Phrase checks can be gamed and do not measure semantic truth. No external model was evaluated.

## Suggested next step

Add your own data and domain-specific acceptance tests. Read and understand the implementation before presenting it in interviews. No live deployment is implied.

<!-- AH-INDEPTH-DOCS:START -->
## In-depth engineering guide

### Problem and scope

A reproducible regression gate for saved model responses.

This is an independent runnable reference implementation, with synthetic sample input and explicit limits. It is not a deployed service or independently validated business result.

### Architecture and end-to-end flow

```text
Saved candidate/baseline answers → case rules → per-case results → aggregate score → regression/release gate
```

| File | Responsibility |
|---|---|
| core.py | Domain validation and project-specific algorithm/state transitions |
| main.py | Bounded JSON CLI input, demo dispatch and JSON output |
| example.json | Exact reproducible sample input |
| tests/test_core.py | Unit and edge-case coverage |

### Design decisions and trade-offs

1. The tool evaluates saved model responses, not model inference. Required/forbidden phrases, citation/refusal checks and JSON-key presence are inspectable deterministic rules.

2. Baseline comparison flags regressions on the same cases. Aggregate scores are meaningful only for this case set and rule configuration; passing a gate does not certify semantic truth, safety or production reliability.

3. JSON structure checks are shallow key checks, not a complete JSON Schema implementation. Phrase matching cannot understand paraphrases, irony or contradictory claims.

### Reproducible setup

Requires Python 3.11+ and no third-party Python packages. Run from this project folder:

```bash
python main.py demo
python main.py run example.json
python -m unittest discover -s tests -v
```

CLI inputs are JSON objects, bounded to 1 MB. Supported domain errors produce a JSON error on stderr and a nonzero exit; inspect the message rather than treating a failed run as a result. The demo does not require a model key, network access or production data.

### Exact example input

```json
{
  "threshold": 1,
  "cases": [
    {
      "id": "cite",
      "must_include": [
        "immutable"
      ],
      "citation": true
    },
    {
      "id": "json",
      "json_keys": [
        "answer",
        "sources"
      ]
    }
  ],
  "candidate": {
    "cite": "Snapshots use immutable blocks [notes:1]",
    "json": "{\"answer\":\"CRC32\", \"sources\":[\"notes\"]}"
  },
  "baseline": {
    "cite": "Blocks are immutable."
  }
}
```

### Core implementation interfaces

| Callable | Boundary |
|---|---|
| `evaluate(c, text)` | Implementation boundary; see source for validation and return structure. |
| `run(p)` | Implementation boundary; see source for validation and return structure. |

The Python `run` result is JSON-serializable. Inspect the source and `main.py run example.json` output for the exact return keys; do not assume another project’s result schema.

### Test coverage and reproducibility

- `tests/test_core.py::test_pass`
- `tests/test_core.py::test_regression`
- `tests/test_core.py::test_json_failure`
- `tests/test_core.py::test_missing`
- `tests/test_core.py::test_no_rules`

5 named tests are present in this folder. Run the command above to reproduce the local test results. Provider calls are mocked; Docker build/run was not executed; no real cloud/model/production-cluster validation is claimed.

### Security and failure boundaries

This is a rule-based LLM evaluation harness, not an LLM and not a comprehensive safety evaluator. It evaluates supplied responses; it does not generate them. Phrase checks can be gamed and do not measure semantic truth. No external model was evaluated.

Never commit .env, real API keys, runtime databases, approval material or customer data. See SECURITY.md. A successful example demonstrates the included workflow, not safe internet deployment.

### Troubleshooting

- **Import error:** run from this project’s own folder; each project intentionally has its own core.py.
- **Invalid sample/schema:** start from example.json, then change one field at a time and read the returned validation message.
- **Port already in use:** stop the previous process or select another --port where server.py exists.
- **SQLite lock/state surprise:** close duplicate processes, confirm PROJECT_DB and back up before deliberate resets. Do not delete unrelated project data.
- **External dependency unavailable:** default demos run offline; live provider calls and container pulls require your own working access and may incur external costs.

### Known limitations

This is a rule-based LLM evaluation harness, not an LLM and not a comprehensive safety evaluator. It evaluates supplied responses; it does not generate them. Phrase checks can be gamed and do not measure semantic truth. No external model was evaluated.

### Extension roadmap — not implemented

Add independently labeled datasets, semantic evaluators, confidence intervals and protected golden-test versioning; keep heuristic scores separate from human review.
<!-- AH-INDEPTH-DOCS:END -->
