# Verification

## Deployed source

- Network: Stable Studionet, chain ID 61999.
- RPC: `https://studio.genlayer.com/api`. Read-only preflight returned `eth_chainId = 0xf22f` and `eth_gasPrice = 0x0`.
- Contract: [0xe304B9019Ba237E3daA1370077546AE6b02b4E58](https://explorer-studio.genlayer.com/address/0xe304B9019Ba237E3daA1370077546AE6b02b4E58).
- Source SHA256: `83a9eb71254c7976fbb473c5c03bc01b5e9c62edd8b97d92cd65ed60e09a1df8`.
- Source checkpoint: [a50e43df218533cfc615193d3497a9a549772fd8](https://github.com/halihalibt/termfence-primitive/commit/a50e43df218533cfc615193d3497a9a549772fd8).
- [Source byte comparison and finalized protocol read](evidence/source-verification.json).
- SDK: `genlayer-js@1.1.8`; pinned contract dependency in the source header.

The hosted RPC does not provide `eth_sendTransaction`. That preliminary transport request returned Method not found and created no transaction. Deployment and all four lifecycle writes used signed raw transactions from a fresh development account, zero value and zero gas price. No external-wallet private key, paid API or faucet funding was used.

## Finalized lifecycle

Every transaction below is `FINALIZED / MAJORITY_AGREE`, with successful leader execution (`return`), Normal consensus and `leader_only=false`.

| Step | Actual result | Transaction |
|---|---|---|
| deployment | Contract deployed | [0xf157dbd7e4…](https://explorer-studio.genlayer.com/tx/0xf157dbd7e4773ab134df81d14769dcefc64b971a2e4817c1f1a5249f0328869f) |
| seal | SEALED, revision 0 | [0x68a379f0b1…](https://explorer-studio.genlayer.com/tx/0x68a379f0b104d001c1dda7e1e06bf3ae5df5d08c7983813186ba84e5e4fcf98e) |
| negative | LOST / LOST; addition NONE; REJECTED, revision 1 | [0x20662a59e4…](https://explorer-studio.genlayer.com/tx/0x20662a59e48b6689805de57d540ea0633ba42571fbc7960c95bbe6dee70d2432) |
| positive | KEPT / KEPT; addition NONE; PRESERVED, revision 2 | [0xadd98d0135…](https://explorer-studio.genlayer.com/tx/0xadd98d0135323e32734c6a21ebf391e8b89d91d4a8e75f796e0a5cff5d3e576f) |
| publish | PUBLISHED, revision 3; selected attempt 1 | [0x59d65f1878…](https://explorer-studio.genlayer.com/tx/0x59d65f18782c53709309f8b2bf9ac054e7ced2ecec41299c14c1699688f6134d) |

The fixture is a **synthetic library-rule example**, not an authenticated public policy. The rejected candidate omitted both the “up to” quantity boundary and the reference-book exception. The passing candidate retains them while using fewer characters.

The positive assessment took **two network consensus rounds and one leader rotation**. In the first round the leader proposed KEPT / LOST; two completing validators disagreed. The next round accepted KEPT / KEPT. The same transaction hash was tracked throughout; no client retransmission or Appeal was performed. This illustrates both substantive validator disagreement and model variability, not universal semantic accuracy.

Deployment, seal and both semantic assessments each show three AGREE and two IDLE votes in the final round; publication shows five AGREE. IDLE is not described as successful semantic verification. Node addresses and hosted model policies do not establish independent operators.

[Final record](evidence/final-record.json) · [Deployment and transaction manifest](deployment.json). Step files preserve the exact submitted arguments and final readbacks. `receipt-*.json` files are clearly labelled RPC field projections: they preserve vote/result fields and every consensus round, omitting repeated source encodings, redundant raw byte arrays and provider configuration. Explorer links provide independent retrieval.

## Offline coverage

Seventeen Python unittest cases passed on 2026-10-26. Models and VM consensus are scripted. Cases cover immutable source, ownership, revision guards, full-vector disagreement, reverse-entailment disagreement, uncertain/malformed/error paths, attempt limits, candidate deduplication, publication eligibility and hash binding. [Recorded scope](evidence/offline.json). These are not real-network accuracy tests.

The live example verifies omission rejection, a preserved paraphrase and terminal publication. Unsupported-addition rejection, ambiguous inputs and adversarial prompt injection have **not** received separate live-network control transactions; local tests do not fill that evidence gap.

## Recheck without writes

```sh
npm ci
npm run verify:live
```

The verifier has no account or signer. It checks the exact deployed source, all five finalized receipts, actual sender and contract, full-consensus mode, final published selection, exact fixture inputs and source/candidate hashes. [Captured output](evidence/live-verification.txt). It sends no transactions.
