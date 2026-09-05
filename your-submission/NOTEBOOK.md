# AI Team Intern Assignment - The Audit

## Day 1 - Baseline Reproduction

Reproduced the previous intern benchmark using `fertility.py` with GPT-2.

- English fertility: 1.27 tok/word
- Hindi fertility: 7.45 tok/word
- Hindi/English ratio: 5.89x

Initial hypothesis: the large Hindi/English gap might be explained by whitespace handling.

## Day 2 - Part A Audit and Dead End

Audited UTF-8 loading, NFC normalization, casing, whitespace, duplicate lines, empty lines, and token/word calculations.

Found that `split(" ")` treats repeated spaces as empty words.

Tested collapsing repeated spaces:

- English fertility: 1.2652 -> 1.2688
- Hindi fertility: 7.4485 -> 7.5785
- Hindi/English ratio: 5.8871 -> 5.9730

Revision: repeated whitespace changes the measurement, but the small change does not explain the overall multilingual gap. The initial hypothesis was rejected as the primary explanation.

Also tested lowercasing:

- Original English fertility: 1.2152
- Lowercased English fertility: 1.2532
- Delta: +0.0380 tok/word

Revision: lowercasing is measurement-changing preprocessing and should not silently alter the production text being benchmarked.

## Day 3 - Corrected Part A Analysis

Corrected the analysis using a 997-sentence aligned FLORES-200 corpus covering English, Hindi, Kannada, and Tamil.

Compared GPT-2 with XLM-R.

Mean input tokens per parallel sentence:

- English: GPT-2 25.82, XLM-R 29.08
- Hindi: GPT-2 192.17, XLM-R 36.75
- Kannada: GPT-2 350.88, XLM-R 39.74
- Tamil: GPT-2 398.36, XLM-R 39.20

Tokenizer comparison:

- English: XLM-R uses 12.6% more tokens than GPT-2
- Hindi: XLM-R uses 80.9% fewer
- Kannada: XLM-R uses 88.7% fewer
- Tamil: XLM-R uses 90.2% fewer

Revision: tokenizer choice, rather than script alone, has a major effect on Indic tokenization.

For routing/cost analysis, use mean input tokens per parallel sentence as the controlled evaluation denominator, then validate against real production input tokens/request.

## Day 3 - Part B Serving Audit

KV bytes/token:

`2 x 8 KV heads x 128 head_dim x 2 bytes x 28 layers = 114,688 bytes/token`

4096-token sequence:

`114,688 x 4096 = 469,762,048 bytes = approximately 0.470 GB`

Usable memory:

`24 x 0.92 - 1.6 = 20.48 GB`

Approximate theoretical maximum:

`20.48 / 0.470 = approximately 43 sequences`

The theoretical estimate does not directly match the observed benchmark KV utilization, so the discrepancy is reported rather than assigned an unsupported exact cause.

For batch 24, prompt 3584, generation 512:

- Reported throughput: 1607.4 tok/s
- Prompt + generation calculation: approximately 1607.33 tok/s
- Decode-only goodput: 12,288 / 61.16 = 200.92 tok/s
- Independent check: 1607.4 x 512 / 4096 = 200.93 tok/s

Revision: `reported_tok_s` includes prompt and generation tokens and should not be interpreted as decode-only throughput.

Long-context anomaly:

- Batch 24: 200.92 tok/s, KV 0.93, 0 preemptions
- Batch 32: 172.99 tok/s, KV 0.97, 7 preemptions
- Batch 48: 162.31 tok/s, KV 0.97, 23 preemptions

Goodput drops 13.90% at batch 32 and 19.21% at batch 48 relative to batch 24.

Recommendation: cap long-prompt scheduling at `max_num_seqs=24`.

## Day 4 - Part C

Initial recommendation: test prompt-only first because it requires no training and adds no separate inference stage.

Evaluation plan:

- 6 target languages
- 50 prompts per language
- 300 total evaluation prompts
- 30 reviewer-hours available over 3 weeks
- At 5 minutes/example: approximately 360 review decisions

Success threshold: at least 90% of reviewed Hindi and Kannada responses should be acceptably casual and linguistically appropriate, with no more than a 5 percentage-point semantic-correctness regression.

Kill criterion: below 85% acceptable-casualness on the initial Hindi/Kannada evaluation by the end of Week 1.

Day-1 experiment: compare current/default prompting against an improved prompt requesting natural, conversational language while preserving meaning.

## Day 5 - Final Revision

1. Do not interpret tokenizer fertility as serving cost without measuring controlled token counts and serving behavior.
2. Use multiple tokenizers and multiple denominators in Part A.
3. Preserve original casing instead of silently lowercasing benchmark input.
4. Use decode-only generated-token goodput for serving capacity decisions.
5. Track KV-cache utilization and preempted sequences.
6. Treat batch 24 as the best observed long-context operating point.
7. Start with prompt-only for Part C and escalate only if the measured quality target is missed.
8. Record failed hypotheses and revisions rather than presenting only successful experiments.
