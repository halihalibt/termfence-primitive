# Verification

## Offline

Seventeen Python unittest cases passed on 2026-10-26. Models and VM consensus are scripted. The cases exercise ownership, immutable source, revision checks, full-vector disagreement, reverse-entailment disagreement, publication eligibility, uncertainty, malformed/error paths, attempt bounds, candidate deduplication and hash binding. They do not establish real-model behavior.

## Stable Studionet preflight

Read-only RPC calls returned chain ID `0xf22f` (61999) and gas price `0x0` on 2026-10-26. Official network documentation identifies `https://studio.genlayer.com/api` as stable Studionet. The preview deployment on chain 61997 is not used.

## Live lifecycle

No live deployment or successful semantic assessment is asserted until final receipts and state readbacks have been captured. See `evidence/` for the recorded network results.
