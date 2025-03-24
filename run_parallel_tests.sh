#!/bin/bash

# Adjust number of parallel jobs to match CPU cores (or limit to something like 4)
JOBS=4

# Export required env vars if needed (like PYTHONPATH, if steps are in subfolders)

# Find all feature files and run them in parallel
find features -name "*.feature" | parallel -j $JOBS "behave {} --no-capture --no-skipped --tags=-@wip"
