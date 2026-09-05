# Part C — Recommendation Memo

## Recommendation

Choose **prompt-only** for casual multilingual responses.

## Assumptions

- The goal is casual multilingual responses.
- We should minimize engineering and serving cost.
- The existing model can already generate responses; the main question is whether additional training or a rewriter is justified.
- A prompt-only approach is the lowest-complexity option and should be tested first.

## Arithmetic / Cost Reasoning

Prompt-only requires no additional model training and no additional rewriter inference stage.

A separate rewriter would add another model inference step, increasing serving cost and latency. SFT would add training cost and operational complexity.

Therefore, prompt-only has the lowest incremental cost and latency, subject to meeting the quality target.

## Success Metric

Run a multilingual evaluation set and measure:

**Target: ≥90% acceptable responses** across the selected languages, while maintaining the existing safety requirements.

## Kill Criterion

If prompt-only achieves **<90% acceptable responses** on the evaluation set, stop relying on prompt-only and evaluate the ≤1B rewriter or SFT alternative.

## Day-1 Experiment

Create a small multilingual evaluation set covering English, Hindi, and the selected Dravidian languages.

Run the same prompts using:
1. Current/default prompting.
2. Improved multilingual prompt instructions.

Record response quality, language correctness, and failure cases.

Compare the results against the 90% success threshold before investing in additional training or a rewriter.

## Decision

Start with prompt-only because it is the cheapest and fastest hypothesis to test. Only move to a rewriter or SFT if the measured quality fails the target.
