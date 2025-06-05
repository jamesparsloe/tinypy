# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TinyPy is a toy Python interpreter implementing a minimal subset of Python, following the tree-walk interpreter pattern from "Crafting Interpreters". The interpreter consists of three main components: tokenizer (lexical analysis), parser (AST generation), and interpreter (tree-walk execution).

## Development Commands

Always use `uv` as our Python package and project manager.

```bash
# Install dependencies
uv sync --all-extras --dev

# Run tests
uv run pytest

# Run all example files (integration tests)
./test.sh

# Run the REPL
uv run tinypy

# Execute a script
uv run tinypy script.py

# Tokenize a file (debugging)
uv run tokenize script.py
```

- When writing git commit messages don't mention that the commit was coauthored by Claude Code - just write a suitable commit message

## Architecture

The codebase follows a classic interpreter pipeline:

1. **Tokenizer** (`src/tinypy/tokenizer.py`): Converts source text to tokens, handling Python-style indentation with INDENT/DEDENT tokens
2. **Parser** (`src/tinypy/parser.py`): Recursive descent parser building an AST using the Visitor pattern
3. **Interpreter** (`src/tinypy/interpreter.py`): Tree-walk interpreter maintaining variable/function state and executing the AST

Key design patterns:

- Visitor pattern for AST traversal
- Dataclasses for AST nodes
- Enum types for token classification
- Separate namespaces for variables and functions in the interpreter

## Testing Strategy

- **Unit tests**: Test individual components (tokenizer, parser, interpreter) using pytest
- **Integration tests**: The `test.sh` script runs all files in `examples/` to ensure they execute without errors
- When adding new features, create an example file in `examples/` and ensure it passes in `test.sh`

## Known Issues & TODOs

- Error handling framework needs implementation
- Whitespace handling has bugs
- Print is currently a statement (should become a function)
- Logical operators (`and`, `or`) are tokenized but not implemented
