# Part A - A4 Decision Memo

## Corrected headline

On the 997-sentence FLORES-200 devset, GPT-2 averages 25.82 English, 192.17 Hindi, 350.88 Kannada, and 398.36 Tamil tokens/sentence. XLM-R averages 29.08, 36.75, 39.74, and 39.20 respectively.

Compared with GPT-2, XLM-R uses 12.6% more tokens for English, but 80.9% fewer for Hindi, 88.7% fewer for Kannada, and 90.2% fewer for Tamil.

## Routing recommendation

Do not use the original 5.89x fertility headline for routing or cost. Use mean input tokens per parallel sentence as the controlled evaluation proxy, and validate it against real production input tokens/request.

For Indic traffic, prefer an Indic-aware or multilingual tokenizer-model stack. In this experiment, XLM-R substantially reduces Indic token counts compared with GPT-2.

## Biggest caveat

FLORES-200 is a translated evaluation corpus, so it controls semantic content across languages but does not represent every production domain, prompt length, code-switching pattern, or conversational style. Token counts are tokenizer-specific and should be validated on real production traffic before capacity or cost commitments.

## Production metric

Track p50/p95 input tokens per request by language and tokenizer/model, together with request volume and latency. This directly connects language mix to serving capacity and cost.
