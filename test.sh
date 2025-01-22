#!/bin/bash

output=$(uv run tinypy examples/fibonacci.py)
if [ "$output" = "55" ]; then
    echo "Test passes!"
else
    echo "Test failed: expected 55 but got '$output'"
fi