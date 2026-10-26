# Protocol

## Public API

| Method | Authorization | Effect |
|---|---|---|
| `seal(slug: str, source_units_json: str)` | Any sender | Creates immutable source, returns record ID |
| `assess(record_id: str, expected_revision: int, candidate: str)` | Record owner | Consensus-backed append, returns full record JSON |
| `publish(record_id: str, expected_revision: int, attempt_index: int)` | Record owner | Selects accepted candidate, returns full record JSON |
| `get_record(record_id: str)` | Public read | Record JSON, or empty string when absent |
| `get_protocol()` | Public read | Version, limits and exact semantic rules |

`source_units_json` is a JSON array encoded as a string, not a variadic argument. Every unit is mandatory. Source unit ordering determines the signal ordering. Candidate indices are zero-based.

## State

SEALED begins at revision 0. An assessment with no accepted candidate produces ASSESSED. Any accepted candidate makes READY; a later rejected attempt does not erase readiness or change earlier findings. Only READY can become PUBLISHED. Publishing increments the revision and permanently freezes the record. No replacement source, editing, revocation or appeal method exists.

An assessment requires the exact current revision, a previously untested candidate and an unexhausted attempt budget. The complete consensus result is obtained before any mutation. Failure leaves the previous record intact through transaction rollback. Only finalized successful execution is authoritative; an accepted intermediate transaction is insufficient.

## Deterministic outcome

| Signals | Outcome |
|---|---|
| Any LOST or addition ADDED | REJECTED |
| Otherwise any UNCLEAR | REVIEW |
| All KEPT and addition NONE | PRESERVED |

The validator independently evaluates the frozen input and compares every label. A leader `LOST,KEPT` and validator `KEPT,LOST` disagree even though both would reject. Model exceptions, malformed responses and non-return VM values reject validation. No failure is silently mapped to a business result.

## Bounds and identity

16 records per owner; 2–8 unique source units, 10–800 Unicode code points each; source JSON at most 10,000 code points; four assessments per record. Candidate length is at least ten code points and strictly less than the sum of source-unit lengths. This is a code-point bound, not a token-cost guarantee. Slugs contain 3–32 lowercase ASCII letters, digits or hyphens.

Source SHA256 binds protocol and ordered source units. Candidate SHA256 binds source hash and exact candidate. Serialization is sorted compact UTF-8 JSON with `ensure_ascii=False`. Hashes establish byte identity, not truth or semantic correctness. Revisions prevent overwriting concurrent updates. Repeated seal/candidate requests reject before model execution. Per-owner quotas do not prevent Sybil usage.

## Runtime

The pinned Python SDK exposes `gl.nondet.exec_prompt(..., response_format="json")`, `gl.vm.Return` and `gl.vm.run_nondet_unsafe`. New SDK previews and chain 61997 are outside this release. Integration tooling must verify `eth_chainId` before any write and must not automatically retransmit failed or uncertain writes.
