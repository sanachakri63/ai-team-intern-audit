# A1 - Corpus Documentation

## Source

Corpus: FLORES-200 dev split, accessed through the `yash9439/flores200` Hugging Face dataset.

## Languages

- English (`eng_Latn`)
- Hindi (`hin_Deva`)
- Kannada (`kan_Knda`)
- Tamil (`tam_Taml`)

Kannada and Tamil provide the two required Dravidian languages.

## Size

The dev split contains 997 aligned sentences for each selected language.

Total selected sentence records:

4 x 997 = 3,988 language-sentence records.

## Domain

FLORES-200 is a multilingual machine-translation evaluation corpus. The selected sentences are translations aligned across languages, making them useful for controlled cross-language tokenization comparison.

## Preprocessing

- Read the selected language columns from the dataset.
- Removed empty records.
- Stripped leading/trailing whitespace.
- Preserved original casing.
- Saved one sentence per line as UTF-8 text.
- Did not intentionally lowercase the corrected A3 corpus.

## Limitations

FLORES-200 is not representative of all production traffic. It may differ from production data in domain, prompt length, conversational style, code-switching, formatting, and vocabulary.

The corpus is translated evaluation text rather than naturally occurring user traffic. Therefore, the results should be treated as a controlled tokenizer comparison, not as a direct prediction of production serving cost.

Production routing decisions should ultimately be validated using real language-specific input-token distributions and serving measurements.
