# AI Team Intern Assignment — The Audit

## Day 1 — Baseline Reproduction

Reproduced the previous intern benchmark using `fertility.py` with GPT-2.

- English fertility: 1.27 tok/word
- Hindi fertility: 7.45 tok/word
- Hindi/English ratio: 5.89×

## Day 2 — Part A Audit

Audited UTF-8 loading, NFC normalization, casing, whitespace, duplicate lines, empty lines, and token/word calculations.

Found a whitespace-sensitive issue: `split(" ")` treats repeated spaces as empty words.

Tested collapsing repeated spaces:
- English fertility: 1.2652 → 1.2688
- Hindi fertility: 7.4485 → 7.5785
- Hindi/English ratio: 5.8871 → 5.9730

The whitespace issue changes the result, but does not explain the overall multilingual gap.

## Day 3 — Part B Serving Audit

KV bytes/token:

`2 × 8 KV heads × 128 head_dim × 2 bytes × 28 layers = 114,688 bytes/token`

4096-token sequence:

`114,688 × 4096 = 469,762,048 bytes ≈ 0.470 GB`

Usable memory:

`24 × 0.92 − 1.6 = 20.48 GB`

Approximate maximum:

`20.48 / 0.470 ≈ 43 sequences`

For batch 24, prompt 3584, generation 512:
- Reported throughput: 1607.4 tok/s
- Prompt + generation calculation: ≈1607.33 tok/s
- Decode-only goodput: 12,288 / 61.16 = 200.92 tok/s
- Independent check: 1607.4 × 512 / 4096 = 200.93 tok/s

Therefore `reported_tok_s` includes prompt tokens and should not be interpreted as decode-only throughput.

Long-context anomaly:
- Batch 24: 200.92 tok/s, KV 0.93, 0 preemptions
- Batch 32: 172.99 tok/s, KV 0.97, 7 preemptions
- Batch 48: 162.31 tok/s, KV 0.97, 23 preemptions

Goodput drops 13.90% at batch 32 and 19.21% at batch 48 relative to batch 24.

## Day 4 — Part C

Recommended prompt-only for casual multilingual responses.

Success metric: ≥90% acceptable responses.

Kill criterion: <90% acceptable responses.

Day-1 experiment: compare current/default prompting against improved multilingual prompting across English, Hindi, and selected Dravidian languages.

## Day 5 — Final Revision

1. Do not interpret tokenizer fertility as serving cost without measuring actual token counts and serving behavior.
2. Use multiple tokenizers and multiple denominators in the corrected Part A analysis.
3. Use decode-only generated-token goodput for serving capacity decisions.
4. Track KV-cache utilization and preempted sequences.
5. Start with prompt-only and escalate only if the measured quality target is missed.
