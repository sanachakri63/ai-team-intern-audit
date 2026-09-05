import unicodedata
import tiktoken

enc = tiktoken.get_encoding("gpt2")
path = "corpus_sample/eng_sample.txt"

with open(path, encoding="utf-8") as f:
    lines = [x.rstrip("\n") for x in f if x.strip()]

def measure(lines, lowercase=True, word_method="space"):
    total_tokens = 0
    total_words = 0
    per_line = []

    for line in lines:
        text = line.lower() if lowercase else line
        tokens = len(enc.encode(text))
        words = len(text.split(" ")) if word_method == "space" else len(text.split())
        total_tokens += tokens
        total_words += words
        per_line.append(tokens / words)

    return total_tokens / total_words, sum(per_line) / len(per_line)

print("A2 AUDIT EXPERIMENTS")

a, _ = measure(lines, lowercase=False)
b, _ = measure(lines, lowercase=True)
print(f"1. Lowercasing: original={a:.4f}, lowercase={b:.4f}, delta={(b-a):.4f}")

a, _ = measure(lines, lowercase=True, word_method="space")
b, _ = measure(lines, lowercase=True, word_method="split")
print(f"2. Repeated-space bug: split(' ')={a:.4f}, split()={b:.4f}, delta={(b-a):.4f}")

_, macro = measure(lines, lowercase=True)
micro, _ = measure(lines, lowercase=True)
print(f"3. Macro vs micro fertility: macro={macro:.4f}, micro={micro:.4f}, delta={(macro-micro):.4f}")

nfc_lines = [unicodedata.normalize("NFC", x) for x in lines]
same = lines == nfc_lines
print(f"4. NFC normalization: changed_text={not same}")

print("5. random.seed(1337): harmless because no random sampling is performed.")
