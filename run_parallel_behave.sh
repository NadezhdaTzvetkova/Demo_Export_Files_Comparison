#!/bin/bash

# Default number of processes if not passed as argument
PROCESSES=${1:-4}

echo "🔄 Running Behave tests in parallel using $PROCESSES processes..."

find features -name "*.feature" | \
xargs -n 1 -P $PROCESSES behave --no-capture --tags "not @skip"

echo "✅ Parallel execution completed!"