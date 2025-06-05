#!/bin/bash

# benchmark.sh - Compare Python vs TinyPy performance on example scripts

set -e

EXAMPLES_DIR="examples"
PYTHON_CMD="python3"
TINYPY_CMD="uv run tinypy"

echo "TinyPy vs Python Performance Benchmark"
echo "======================================"
echo

# Check if examples directory exists
if [ ! -d "$EXAMPLES_DIR" ]; then
    echo "Error: examples directory not found"
    exit 1
fi

echo "Running benchmarks on all example files..."
echo

total_python_time=0
total_tinypy_time=0
file_count=0

# Benchmark each Python file in examples
for file in "$EXAMPLES_DIR"/*.py; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        
        echo "Benchmarking: $filename"
        echo "------------------------"
        
        # Time Python execution using bash built-in time
        echo -n "Python:  "
        { time $PYTHON_CMD "$file" > /dev/null 2>&1; } 2>&1 | grep real | awk '{print $2}'
        
        # Time TinyPy execution using bash built-in time
        echo -n "TinyPy:  "  
        { time $TINYPY_CMD "$file" > /dev/null 2>&1; } 2>&1 | grep real | awk '{print $2}'
        
        echo
        file_count=$((file_count + 1))
    fi
done
