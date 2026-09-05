import pandas as pd

df = pd.read_csv("partA/corrected_metrics.csv")

print("\n=== CORRECTED A3 RESULTS ===")
print(df[["lang","tokenizer","tok_per_sentence","tok_per_word","tok_per_grapheme","tok_per_byte"]].round(3).to_string(index=False))

print("\n=== TOKENIZER COMPARISON ===")
for lang in ["eng","hin","kan","tam"]:
    g = df[(df.lang == lang) & (df.tokenizer == "gpt2")].iloc[0]
    x = df[(df.lang == lang) & (df.tokenizer == "xlm-roberta-base")].iloc[0]
    improvement = (g.tok_per_sentence - x.tok_per_sentence) / g.tok_per_sentence * 100
    print(f"{lang}: XLM-R uses {abs(improvement):.1f}% " + ("more" if improvement < 0 else "fewer") + " tokens/sentence than GPT-2")

print("\n=== ROUTING NUMBER ===")
print("Use mean input tokens per parallel sentence as the routing/cost denominator.")
