# TermFence

A standalone GenLayer Intelligent Contract for **material-fact preservation in compressed text**. Seal an ordered source, test shorter candidates, and publish only a candidate whose full preservation vector and absence of unsupported additions have passed independent validator assessment.

Useful for agent handoff summaries, compact operational instructions and brief public notices. It creates a shared, immutable acceptance record that downstream developers can read without trusting a summarization server. It does not generate the summary or authenticate the source.

## Mechanism

1. `seal(slug, source_units_json)` fixes 2–8 mandatory source units in the caller's namespace.
2. `assess(record_id, expected_revision, candidate)` independently evaluates every source unit against the shorter candidate and checks the entire candidate for unsupported additions.
3. The leader and each validator run the same semantic task independently. Every ordered `KEPT / LOST / UNCLEAR` label and the separate `NONE / ADDED / UNCLEAR` addition label must match. Agreement on just the aggregate result is insufficient.
4. Deterministic code derives `PRESERVED`, `REJECTED` or `REVIEW`, appends the attempt and increments the revision. Any loss or addition rejects; uncertainty cannot pass.
5. `publish(record_id, expected_revision, attempt_index)` permanently selects a PRESERVED candidate. The record then becomes terminal.

Negation, permission versus obligation, responsible actor, quantities, boundaries, conditions and exceptions are explicitly material. Rephrasing and merging are allowed; weakening an exception is not. The reverse addition check prevents a candidate from keeping the required facts while inventing a new benefit or promise.

## Reuse

Deploy the complete single-file [contract](contracts/term_fence.py), with no constructor arguments. All writes use the actual sender address. Read `get_protocol()` and `get_record(record_id)` as JSON strings. The record ID is `<lowercase-owner-address>:<slug>`.

[API, state and limits](PROTOCOL.md) · [Call examples](examples/library.json) · [Security and limitations](SECURITY.md) · [Network evidence](EVIDENCE.md).

Run offline checks with Python 3.12+:

```sh
python -m unittest discover -s tests -v
```

The tests replace the model and GenLayer boundary with scripted responses. They verify state and rejection behavior, **not real model accuracy or network consensus**. Live receipts, when available, are recorded separately in `evidence/`.

Stable Studionet only: chain `61999`, RPC `https://studio.genlayer.com/api`. The contract's dependency is pinned in its first line. No frontend, backend, API key, token sale, fund custody or application companion is required. MIT licensed.
