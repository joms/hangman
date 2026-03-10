#!/usr/bin/env python3
"""One-time script to extract unique words from lemma.txt into words.txt.gz."""

import gzip
from pathlib import Path

src = Path(__file__).parent / "lemma.txt"
dst = Path(__file__).parent / "words.txt.gz"

words = set()
with open(src, encoding="latin-1") as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        parts = line.strip().split("\t")
        if len(parts) < 3:
            continue
        word = parts[2]
        if word.startswith("-") or not word.isalpha():
            continue
        words.add(word)

with gzip.open(dst, "wt", encoding="utf-8") as f:
    for word in sorted(words):
        f.write(word + "\n")

print(f"Wrote {len(words)} unique words to {dst}")
