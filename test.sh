#!/bin/bash

echo "REPL tests"
echo ""

# Run all example scripts and check exit codes
passes=0
failures=0

for script in examples/*.py; do
    output=$(uv run tinypy "$script" 2>&1)
    status=$?
    
    if [ $status -eq 0 ]; then
        echo -e "\033[32m✓ $script passed\033[0m"
        ((passes++))
    else
        echo -e "\033[31m✗ $script failed\033[0m"
        ((failures++))
    fi
done

echo ""
echo -e "\033[32m$passes passed\033[0m \033[31m$failures failed\033[0m"

if [ $failures -gt 0 ]; then
    exit 1
else
    exit 0
fi

# output=$(uv run tinypy examples/fibonacci.py)

# if [ "$output" = "55" ]; then
#     echo "Test passes!"
#     exit 0
# else
#     echo "Test failed: expected 55 but got '$output'"
#     exit 1
# fi