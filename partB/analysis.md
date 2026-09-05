# Part B — Serving Audit

## B1. KV-cache memory

KV bytes/token = 2 × KV_heads × head_dim × bytes(fp16) × layers

= 2 × 8 × 128 × 2 × 28 = 114,688 bytes/token.

For a 4096-token sequence:

114,688 × 4096 = 469,762,048 bytes ≈ 0.470 GB.

Usable memory = 24 × 0.92 − 1.6 = 20.48 GB.

Approximate maximum concurrent 4096-token sequences = 20.48 / 0.470 ≈ 43.

## B2. Throughput audit

For batch 24, prompt 3584, generation 512:

Generated tokens = 24 × 512 = 12,288.

Decode-only goodput = 12,288 / 61.16 = 200.92 tok/s.

The reported 1607.4 tok/s is actually prompt + generation throughput:

24 × (3584 + 512) / 61.16 ≈ 1607.33 tok/s.

Independent check:

1607.4 × 512 / (3584 + 512) = 200.93 tok/s.

Therefore, honest decode-only goodput is approximately 200.9 tok/s.

## B3. Long-context anomaly

Batch 24: 200.92 tok/s, KV utilization 0.93, preempted sequences 0.

Batch 32: 172.99 tok/s, KV utilization 0.97, 7 preemptions.

Batch 48: 162.31 tok/s, KV utilization 0.97, 23 preemptions.

Goodput drops 13.90% at batch 32 and 19.21% at batch 48 relative to batch 24.

Conclusion: throughput peaks at batch 24 and then falls as KV-cache pressure and preemption appear.

## B4. Recommendation

Do not plan capacity using the reported_tok_s column as decode throughput. Use decode-only generated-token goodput and track KV-cache utilization and preempted sequences. Batch 24 is the best observed long-prompt operating point in this benchmark.

