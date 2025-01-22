import tokenize

with open("examples/fibonacci.py", "rb") as f:
    for token in tokenize.tokenize(f.readline):
        print(token)
