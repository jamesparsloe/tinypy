#!/bin/bash

output=$(uv run tinypy examples/fibonacci.py)
if [ "$output" = "55" ]; then
    echo "Test passes!"
    exit 0
else
    echo "Test failed: expected 55 but got '$output'"
    exit 1
fi