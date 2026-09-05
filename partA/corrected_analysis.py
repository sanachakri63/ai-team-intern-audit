import tiktoken, regex, csv
from transformers import AutoTokenizer

enc = tiktoken.get_encoding("gpt2")
tok = AutoTokenizer.from_pretrained("xlm-roberta-base")
langs = ["eng", "hin", "kan", "tam"]

rows = []

for lang in langs:
    with open(f"partA/corpus/{lang}.txt", encoding="utf-8") as f:
        lines = [x.strip() for x in f if x.strip()]

    words = sum(len(x.split()) for x in lines)
    graphemes = sum(len(regex.findall(r"\X", x)) for x in lines)
    byte_count = sum(len(x.encode("utf-8")) for x in lines)

    for name, encode in [
        ("gpt2", lambda x: enc.encode(x)),
        ("xlm-roberta-base", lambda x: tok.encode(x, add_special_tokens=False))
    ]:
        tokens = sum(len(encode(x)) for x in lines)
        rows.append([lang, name, len(lines), tokens, words, graphemes, byte_count])

with open("partA/corrected_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["lang","tokenizer","sentences","tokens","words","graphemes","bytes"])
    writer.writerows(rows)

print("Saved partA/corrected_results.csv")
for r in rows:
    print(r)
