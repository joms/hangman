#!/usr/bin/env python3
import argparse
import os
import random

from random_ord import load_words

STAGES = [
    """
  -----
  |   |
      |
      |
      |
      |
=========""",
    """
  -----
  |   |
  O   |
      |
      |
      |
=========""",
    """
  -----
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  -----
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  -----
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  -----
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  -----
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]

MAX_WRONG = len(STAGES) - 1


def display(word, guessed, wrong, stage):
    os.system("cls" if os.name == "nt" else "clear")
    print(STAGES[stage])
    print()
    print(" ".join(ch.upper() if ch in guessed else "_" for ch in word))
    print()
    if wrong:
        print(", ".join(w.upper() for w in wrong))
    print()


def main():
    parser = argparse.ArgumentParser(description="Hangman med norske ord")
    parser.add_argument("--min-length", type=int, default=6, help="Minimum ordlengde (default: 6)")
    parser.add_argument("--length", type=int, help="Eksakt ordlengde")
    args = parser.parse_args()

    words = load_words(min_length=args.min_length, length=args.length)
    if not words:
        if args.length:
            print(f"Ingen ord funnet med lengde {args.length}")
        else:
            print(f"Ingen ord funnet med minimumslengde {args.min_length}")
        return

    word = None
    while word is None:
        candidates = random.sample(words, min(10, len(words)))
        print("Velg et ord:\n")
        for i, w in enumerate(candidates, 1):
            print(f"  {i:2}. {w.capitalize()}")
        print()
        while True:
            try:
                choice = input("Velg nummer (1-10), eller 'r' for ny liste: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if choice == "r":
                print()
                break
            if choice.isdigit() and 1 <= int(choice) <= len(candidates):
                word = candidates[int(choice) - 1].lower()
                break
            print("Ugyldig valg, prøv igjen.")

    guessed = set()
    wrong = []
    stage = 0

    while stage < MAX_WRONG:
        display(word, guessed, wrong, stage)

        if all(ch in guessed for ch in word):
            print("Du vant!")
            return

        try:
            guess = input("Gjett en bokstav: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not guess.isalpha():
            continue

        if len(guess) > 1:
            if guess == word:
                guessed.update(word)
            else:
                wrong.append(guess)
                stage += 1
            continue

        if guess in guessed or guess in wrong:
            print(f"Du har allerede gjettet '{guess}'.")
            try:
                input("Trykk Enter for å fortsette...")
            except (EOFError, KeyboardInterrupt):
                print()
                return
            continue

        if guess in word:
            guessed.add(guess)
        else:
            wrong.append(guess)
            stage += 1

    display(word, guessed, wrong, stage)
    print(f"Du tapte! Ordet var: {word.upper()}")


if __name__ == "__main__":
    main()
