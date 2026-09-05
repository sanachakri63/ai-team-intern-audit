# A2 - Audit Results

## 1. Lowercasing is a measurement-changing code bug
Experiment: run the same English corpus with original casing versus lowercase normalization.
Result: corpus fertility changes from 1.2152 to 1.2532 tokens/word, a +0.0380 absolute change.
Why it matters: fertility is being measured after silently modifying the input, so the benchmark does not measure the original production text.

## 2. split(" ") mishandles repeated whitespace
Experiment: compare the starter metric's split(" ") with split().
Result: fertility changes from 1.2532 to 1.2692 tokens/word, a +0.0161 absolute change.
Why it matters: repeated spaces create empty pseudo-words, changing the denominator.

## 3. Per-line averaging differs from corpus-level fertility
Experiment: compare the mean of per-line token/word ratios with total tokens divided by total words.
Result: macro fertility = 1.2652 versus micro fertility = 1.2532, a 0.0120 difference.
Why it matters: the starter code gives every line equal weight rather than weighting by its actual word count.

## 4. Conceptual flaw: tokens/whitespace-word is not the routing/cost denominator
The code correctly computes tokens per whitespace-delimited word, but whitespace-word counts are not a controlled unit of equivalent multilingual content. On the aligned 997-sentence corpus, the same semantic sentence count is fixed across languages. Therefore, mean tokens per parallel sentence is the more appropriate controlled proxy for input-token cost.

## 5. Suspicious but fine: NFC normalization
Experiment: compare the corpus before and after Unicode NFC normalization.
Result: changed_text=False.
Why it is fine: NFC normalization did not alter this corpus and is a reasonable defensive normalization step for Unicode text.

## 6. Suspicious but harmless: random.seed(1337)
The starter code sets a random seed, but no random sampling is performed. Therefore the seed has no effect on the reported result.



