# tinypy

A toy version of Python. For now I'm doing the absolute minimum to make `examples/fibonacci.py` work and then I'll expand to a slightly bigger subset of Python and see where I get to.

## Getting Started

```sh
uv sync --all-extras --dev
uv run tinypy -v
```

## Testing

```sh
uv run pytest
```

and also REPL tests

```sh
chmod +x test.sh
./test.sh
```

## TODO

- [ ] Error handling
  - [ ] Syntax errors
  - [ ] Runtime errors
