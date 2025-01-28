"""Actual Python tokenizer to compare against."""

import tokenize
import sys

with open(sys.argv[1], "rb") as f:
    for token in tokenize.tokenize(f.readline):
        print(token)
