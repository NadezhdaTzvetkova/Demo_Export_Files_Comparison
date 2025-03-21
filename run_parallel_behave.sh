#!/bin/bash

# Default number of processes if not passed as argument
PROCESSES=${1:-4}

echo "🔄 Running Behave tests in parallel using $PROCESSES processes..."

# Find all feature files and execute in parallel
find features -name "*.feature" -print0 | xargs -0 -n 1 -P "$PROCESSES" behave --no-capture --tags "not @skip"

echo "✅ Parallel execution completed!"
