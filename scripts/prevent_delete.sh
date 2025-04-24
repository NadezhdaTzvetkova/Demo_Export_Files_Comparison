#!/usr/bin/env bash

# ============================================
# 🛡️ Git Pre-commit Hook: Prevent File Deletion
# ============================================
# Blocks accidental deletion of key files and directories
# Used as a local pre-commit hook in `.pre-commit-config.yaml`

# --------------------------------------------
# 📌 List of protected individual files
# --------------------------------------------
CRITICAL_FILES=(
  "requirements.txt"
  "requirements-dev.txt"
  "requirements.in"
  "requirements-dev.in"
  "pyproject.toml"
  ".pre-commit-config.yaml"
  ".setup_env.sh"
)

# --------------------------------------------
# 📁 List of protected directories (relative paths)
# --------------------------------------------
CRITICAL_DIRS=(
  "features"
  "helpers"
  "scripts"
  "steps"
  "utils"
)

# --------------------------------------------
# ❌ Block deletion of critical files
# --------------------------------------------
for file in "${CRITICAL_FILES[@]}"; do
  if git diff --cached --name-only --diff-filter=D | grep -qx "$file"; then
    echo ""
    echo "❌ ERROR: You are attempting to delete a critical file: '$file'"
    echo "🛑 This file is required for your project’s setup and reproducibility."
    echo ""
    exit 1
  fi
done

# --------------------------------------------
# ❌ Block deletion of any files inside protected directories
# --------------------------------------------
for dir in "${CRITICAL_DIRS[@]}"; do
  if git diff --cached --name-only --diff-filter=D | grep -q "^${dir}/"; then
    echo ""
    echo "❌ ERROR: Attempted deletion detected in protected directory: '$dir/'"
    echo "🛑 This directory contains essential project logic or tests and must not be removed."
    echo ""
    exit 1
  fi
done

# ✅ Everything is safe
exit 0
