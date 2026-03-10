#!/usr/bin/env python3
import argparse
import random
from pathlib import Path


def load_words(min_length=6, length=None):
    lemma_path = Path(__file__).parent / "lemma.txt"
    words = []

    with open(lemma_path, encoding="latin-1") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            word = parts[2]
            if word.startswith("-") or not word.isalpha():
                continue
            if length is not None:
                if len(word) == length:
                    words.append(word)
            elif len(word) >= min_length:
                words.append(word)

    return words


def main():
    parser = argparse.ArgumentParser(description="Pick random Norwegian words for hangman")
    parser.add_argument("-n", type=int, default=1, help="Number of words to pick (default: 1)")
    parser.add_argument("--min-length", type=int, default=6, help="Minimum word length (default: 6)")
    args = parser.parse_args()

    words = load_words(args.min_length)

    if not words:
        print(f"No words found with minimum length {args.min_length}")
        return

    count = min(args.n, len(words))
    for word in random.sample(words, count):
        print(word)


if __name__ == "__main__":
    main()
