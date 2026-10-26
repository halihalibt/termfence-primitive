# Design rationale

TermFence addresses asymmetric compression loss: a short text can retain the main topic while deleting a small but binding exception. Shared keywords or high text similarity cannot establish preservation. A second direction matters too: keeping every mandatory sentence does not excuse adding an unsupported promise.

The primitive therefore fixes one source and evaluates two obligations: each mandatory source unit must survive in the candidate, and every material candidate claim must follow from the source. A candidate must actually be shorter. This is distinct from classifying amendments between evolving versions, matching two parties' requirements, assessing evidence provenance, or deciding whether a migration guide gives actionable instructions. There is no consent epoch, negotiation, source relationship graph or migration-action coverage algorithm.

The deterministic publication gate is the reusable output. Consumers can accept only PUBLISHED records, retrieve the exact selected candidate, and bind it to the protocol and source hash. Rejected candidates are retained for inspection; a later rejection cannot erase a previously accepted option. Every write is revision-bound, source text cannot change, and publication is terminal.

All semantic labels affect acceptance. A validator independently reconstructs the complete ordered preservation vector and reverse-entailment label. Accepting a matching overall verdict would conceal disagreements about which units were lost. The contract stores no free-form leader rationale that validators have not checked.

This design deliberately leaves source decomposition to the caller. Automatically generating a purportedly complete fact list would add another consensus task and a new completeness assumption. The guarantees concern only the exact declared source, under fallible model interpretation on a hosted development network.
