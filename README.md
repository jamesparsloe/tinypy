# tinypy

A toy version of Python. For now I'm doing the absolute minimum to make `examples/fibonacci.py` work and then I'll expand to a slightly bigger subset of Python and see where I get to. I'm somewhat following along with the _Crafting Interpreters_ tree-walk interpreter design.

## Getting started

```sh
uv sync --all-extras --dev
uv run tinypy -v
uv run tinypy examples/statements.py
```

## Testing

```sh
uv run pytest
./test.sh
```
