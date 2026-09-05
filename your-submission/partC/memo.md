# Part C - Recommendation Memo

## Recommendation

Choose **prompt-only** as the first approach for making responses more casual in Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi.

## Assumptions

- Launch review is in 3 weeks.
- One native-speaker reviewer is available for 10 hours/week, giving 30 reviewer-hours before launch review.
- Assume 5 minutes per reviewed example, giving 12 examples/hour and approximately 360 review decisions over 30 hours.
- The reviewer can directly review Hindi and Kannada only. Quality evidence for Tamil, Telugu, Bengali, and Marathi therefore remains a limitation.
- One A100-80GB is available for 2 weeks = 14 x 24 = 336 A100-hours.
- Assume an internal opportunity cost of $2.50/A100-hour, so the full available GPU budget is approximately $840. This is an assumption, not a provided price.
- Prompt-only requires 0 training pairs and 0 additional training GPU-hours.
- The evaluation set will contain 300 prompts: 50 prompts per language.

## Back-of-the-envelope arithmetic

Evaluation volume:

6 languages x 50 prompts = 300 prompts.

Reviewer capacity:

30 hours x 60/5 = 360 reviewed examples.

A 300-prompt evaluation therefore fits within the available reviewer capacity if each example takes about 5 minutes. Since the reviewer is native-speaker qualified only for Hindi and Kannada, prioritize human review for those two languages.

Training cost:

Prompt-only training data = 0 pairs.

Prompt-only training GPU-hours = 0.

SFT would require preparing synthetic training pairs and using part of the 336 available A100-hours. A separate rewriter would also add an additional inference stage and therefore additional serving latency and compute.

## Success threshold

Prompt-only is successful if at least **90% of reviewed Hindi and Kannada responses are rated acceptably casual and linguistically appropriate**, with no more than a 5 percentage-point regression in semantic correctness versus the baseline.

## Kill criterion and deadline

By the **end of Week 1**, stop pursuing prompt-only if the human-rated acceptable-casualness rate is below **85%** on the initial Hindi/Kannada evaluation.

If the rate is 85-90%, run the expanded evaluation through Week 2. If it remains below 90% after the expanded evaluation, move to the <=1B rewriter as the next option.

## Day-1 experiment

Create 60 evaluation prompts: 10 prompts for each of the six target languages.

For every prompt, compare:

1. Current/default prompting.
2. A prompt explicitly requesting natural, conversational, everyday language while preserving meaning.

Measure casualness, language correctness, semantic fidelity, and failure cases. Blind the Hindi/Kannada outputs before reviewer scoring where practical.

The first decision gate is whether the improved prompt produces a meaningful improvement over the baseline and reaches the 90% success target without a semantic-quality regression.

## Decision

Start with prompt-only because it has zero training cost, no additional model-serving stage, and can be tested immediately. If the Week-1 evidence fails the kill criterion, move to the <=1B rewriter rather than spending the remaining schedule on an approach that has already missed the required quality threshold.
