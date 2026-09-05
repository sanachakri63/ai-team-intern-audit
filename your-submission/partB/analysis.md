# Part B - Serving Audit

## B1. KV-cache memory

KV bytes/token:

2 x KV_heads x head_dim x bytes(fp16) x layers

= 2 x 8 x 128 x 2 x 28
= 114,688 bytes/token.

For a 4096-token sequence:

114,688 x 4096
= 469,762,048 bytes
= approximately 0.470 GB.

Usable GPU memory:

24 x 0.92 - 1.6
= 20.48 GB.

Approximate maximum concurrent 4096-token sequences:

20.48 / 0.470
= approximately 43 sequences.

The benchmark log does not match this theoretical estimate directly: at batch 24, KV utilization is 0.93, which corresponds to about 24 / 0.93 = 25.8 batch-equivalents. This gap should be treated as an accounting/scheduler/allocator discrepancy rather than assigning an unsupported exact cause.

## B2. Long-context throughput anomaly

The long-prompt workload uses a 3584-token prompt and 512 generated tokens.

Reported throughput peaks at batch 24 and then decreases:

- Batch 24: 1607.4 tok/s
- Batch 32: 1384.0 tok/s
- Batch 48: 1298.5 tok/s

At the same time, KV utilization and preempted sequences increase:

- Batch 24: KV 0.93, preempted 0
- Batch 32: KV 0.97, preempted 7
- Batch 48: KV 0.97, preempted 23

Decode-only goodput also decreases:

- Batch 24: 200.92 tok/s
- Batch 32: 172.99 tok/s
- Batch 48: 162.31 tok/s

Relative to batch 24, this is a 13.90% drop at batch 32 and a 19.21% drop at batch 48.

The evidence is consistent with KV-cache pressure and preemption becoming the limiting mechanism.

Recommended deployment change: cap long-prompt scheduling at max_num_seqs=24.

Using the observed benchmark, this would improve decode goodput by approximately 16.15% versus batch 32 and 23.78% versus batch 48, while avoiding the observed preempted sequences at batch 24.

## B3. Misread throughput column

The reported_tok_s column is total prompt-plus-generation throughput, not decode-only throughput.

For batch 24:

24 x (3584 + 512) / 61.16
= approximately 1607.33 tok/s,

which matches the reported 1607.4 tok/s.

The honest decode-only goodput is:

24 x 512 / 61.16
= 200.92 tok/s.

Independent derivation:

1607.4 x 512 / 4096
= 200.93 tok/s.

Therefore, the report should not have described 1607.4 tok/s as decode throughput. Longer prompts increase the reported total-token throughput because prompt-processing tokens are included.

## B4. Confirmation metric

Use preempted sequence count/rate as the single confirming metric for the proposed KV-pressure mechanism.

Expected benchmark values:

- Batch 24: 0 preempted sequences
- Batch 32: 7 preempted sequences = 21.9% of 32
- Batch 48: 23 preempted sequences = 47.9% of 48

If the mechanism is correct, increasing long-context batch size beyond the safe operating point should cause preemption to increase while decode goodput falls.

Note: preempted_seqs counts sequences that were preempted, not necessarily the total number of preemption events.
