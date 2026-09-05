import pandas as pd

df = pd.read_csv("partA/corrected_results.csv")
df["tok_per_sentence"] = df.tokens / df.sentences
df["tok_per_word"] = df.tokens / df.words
df["tok_per_grapheme"] = df.tokens / df.graphemes
df["tok_per_byte"] = df.tokens / df.bytes

df.to_csv("partA/corrected_metrics.csv", index=False)

print("Saved partA/corrected_metrics.csv")
