# AI Usage

AI tools were used as a development and auditing assistant.

## Uses

- Helped inspect and understand the starter-kit files.
- Helped reproduce the baseline tokenizer benchmark.
- Helped identify and test the whitespace-sensitive `split(" ")` behavior.
- Helped calculate KV-cache memory requirements.
- Helped audit the meaning of the `reported_tok_s` throughput column.
- Helped calculate decode-only goodput and verify it independently.
- Helped compare GPT-2 and XLM-R on the multilingual corpus.
- Helped organize the audit findings and recommendations into the required deliverables.

## Verification

All important numerical claims were checked by running Python commands against the supplied files. The commands and resulting numbers are recorded in `NOTEBOOK.md` and the Part B analysis.

AI-generated suggestions were treated as hypotheses and verified against the provided benchmark data before being used in the conclusions.

## Example of AI-assisted revision

An initial hypothesis was that repeated whitespace might explain the large Hindi/English fertility gap. The experiment changed the ratio only from 5.8871x to 5.9730x, so the hypothesis was rejected as the primary explanation.

The final conclusions were based on measured experiment results rather than unverified AI suggestions.
