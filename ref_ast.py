import ast
import sys

with open(sys.argv[1], "r") as f:
    source = f.read()

tree = ast.parse(source)
print(ast.dump(tree, indent=2))
