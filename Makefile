.PHONY: \
	# Environment Setup
	setup setup_env check_venv check-env \
	# Dependencies
	install install-dev lock upgrade \
	# Testing
	test allure-report \
	# Code Quality
	format lint check-style check-code type-check \
	pre-commit-run pre-commit-update ci-check help \
	# Maintenance
	clean security-audit reinstall \
	# Git / Bootstrap
	install-lfs bootstrap init

# =============================
# 🔍 PLATFORM DETECTION
# =============================

OS_UNAME := $(shell uname | tr '[:upper:]' '[:lower:]')
ifeq ($(OS),Windows_NT)
	OS_NAME := windows_nt
else
	OS_NAME := $(OS_UNAME)
endif
PYTHON := python3
CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

ifeq ($(OS_NAME), darwin)
	VENV_ACTIVATE := .venv/bin/activate
	VENV_PYTHON := .venv/bin/python
endif
ifeq ($(OS_NAME), linux)
	VENV_ACTIVATE := .venv/bin/activate
	VENV_PYTHON := .venv/bin/python
endif
ifeq ($(OS_NAME), mingw32)
	VENV_ACTIVATE := .venv/Scripts/activate
	VENV_PYTHON := .venv/Scripts/python
endif
ifeq ($(OS_NAME), msys)
	VENV_ACTIVATE := .venv/Scripts/activate
	VENV_PYTHON := .venv/Scripts/python
endif

# =============================
# 🌱 ENVIRONMENT MANAGEMENT
# =============================

check_venv:  ## Check if a virtualenv is active
	@echo "🔍 Checking if a virtual environment is already active..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "⚠️  Active virtualenv detected: $$VIRTUAL_ENV"; \
		echo "❌ Please deactivate it before running this script."; \
		exit 1; \
	else \
		echo "✅ No active virtualenv detected."; \
	fi

setup_env: check_venv  ## Set up Python virtual environment
	@echo "🚀 Creating virtual environment in .venv..."
	@test -d .venv || $(PYTHON) -m venv .venv
	@echo "⬆️  Upgrading pip..."
	@. $(VENV_ACTIVATE) && pip install --upgrade pip
	@echo "📦 Installing pip-tools and pre-commit..."
	@. $(VENV_ACTIVATE) && pip install pip-tools pre-commit
	@echo "✅ Setup complete. Run: source $(VENV_ACTIVATE)"

check-env:  ## Check Python version and venv presence
	@echo "🔍 Checking .venv and Python version..."
	@if [ ! -d ".venv" ]; then \
		echo "❌ .venv not found. Please run: make setup_env"; \
		exit 1; \
	fi
	@echo "✅ .venv exists."
	@echo "🐍 Validating Python version..."
	@. $(VENV_ACTIVATE) && $(VENV_PYTHON) --version | grep '3.11' >/dev/null || \
		(echo '❌ Python is not 3.11.x' && exit 1)

setup:  ## Full setup via .setup_env.sh (optional)
	@echo "⚙️ Running environment setup..."
	@./.setup_env.sh || echo "⚠️ .setup_env.sh missing or failed"
	@$(MAKE) install-lfs

# =============================
# 📦 DEPENDENCY MANAGEMENT
# =============================

install:  ## Install runtime dependencies
	@echo "📦 Installing runtime dependencies..."
	@. $(VENV_ACTIVATE) && pip install -r requirements.txt

install-dev:  ## Install development dependencies
	@echo "🔧 Installing dev dependencies..."
	@. $(VENV_ACTIVATE) && pip install -r requirements-dev.txt

lock:  ## Lock and generate requirements.txt / requirements-dev.txt
	@echo "🔒 Locking runtime and dev dependencies..."
	@. $(VENV_ACTIVATE) && pip-compile --output-file=requirements.txt requirements.in
	@. $(VENV_ACTIVATE) && pip-compile --output-file=requirements-dev.txt requirements-dev.in

upgrade:  ## Upgrade and relock dependencies
	@echo "⬆️  Upgrading requirements and locking them..."
	@. $(VENV_ACTIVATE) && pip-compile --upgrade --output-file=requirements.txt requirements.in
	@. $(VENV_ACTIVATE) && pip-compile --upgrade --output-file=requirements-dev.txt requirements-dev.in
	@echo "✅ Dependencies upgraded and locked."

# =============================
# 🧪 TESTING & REPORTING
# =============================

test:  ## Run tests with behave-parallel and Allure output
	@echo "🧪 Running BDD tests with behave-parallel..."
	@. $(VENV_ACTIVATE) && behave-parallel -n 4 -f allure_behave.formatter:AllureFormatter -o allure-results/behave $(TAGS)

allure-report:  ## Generate Allure test report
	@echo "📊 Generating Allure report..."
	@. $(VENV_ACTIVATE) && allure generate allure-results/behave --clean -o allure-report
	@echo "✅ Report at: allure-report/index.html"

# =============================
# 🎨 CODE QUALITY & FORMATTERS
# =============================

format:  ## Auto-format code with black and ruff
	@echo "🎨 Formatting code..."
	@. $(VENV_ACTIVATE) && black . || true
	@. $(VENV_ACTIVATE) && ruff check . --fix || true

lint:  ## Run ruff lint checks
	@echo "🔍 Running ruff lint..."
	@. $(VENV_ACTIVATE) && ruff check . || true

check-style:  ## Check format with ruff (no fix)
	@echo "🔎 Checking code style..."
	@. $(VENV_ACTIVATE) && ruff check . || true
	@. $(VENV_ACTIVATE) && ruff format --check . || true

type-check:  ## Run mypy (non-blocking)
	@echo "📦 Running mypy (non-blocking)..."
	@. $(VENV_ACTIVATE) && mypy . || true

check-code:  ## Run all non-blocking code checks
	@echo "🛠️ Running all code checks (non-blocking)..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) type-check

ci-check:  ## Run all checks strictly for CI (blocking)
	@echo "🚨 Running CI checks (blocking)..."
	@. $(VENV_ACTIVATE) && ruff check .
	@. $(VENV_ACTIVATE) && ruff format --check .
	@. $(VENV_ACTIVATE) && mypy .

pre-commit-run:  ## Run pre-commit checks on all files
	@echo "🧼 Running pre-commit on all files..."
	@. $(VENV_ACTIVATE) && pre-commit run --all-files || true

pre-commit-update:  ## Update all pre-commit hook versions
	@echo "📦 Updating pre-commit hook versions..."
	@. $(VENV_ACTIVATE) && pre-commit autoupdate
	@echo "✅ Hooks updated!"

# =============================
# 🚀 PROJECT INIT: ONE-STEP SETUP
# =============================

init:  ## One-step: setup, install, hooks, LFS
	@echo "🚀 Initializing project..."
	@$(MAKE) setup_env
	@$(MAKE) lock
	@$(MAKE) install
	@$(MAKE) install-dev
	@$(MAKE) install-lfs
	@echo "🔧 Installing pre-commit hooks..."
	@. $(VENV_ACTIVATE) && pre-commit install
	@. $(VENV_ACTIVATE) && pre-commit autoupdate
	@echo "✅ Project initialized. Run: source $(VENV_ACTIVATE)"

# =============================
# 🧹 CLEANUP & SECURITY
# =============================

clean:  ## Clean up project artifacts and venv
	@echo "🧹 Cleaning up..."
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml .venv *.lock

security-audit:  ## Run pip-audit for security
	@echo "🛡️ Running pip-audit..."
	@. $(VENV_ACTIVATE) && pip install pip-audit >/dev/null
	@. $(VENV_ACTIVATE) && pip-audit || echo "⚠️ Vulnerabilities found."

# =============================
# ♻️ FULL REINSTALL
# =============================

reinstall:  ## Reinstall project from scratch
	@echo "💣 Reinstalling everything..."
	rm -rf .venv requirements.txt requirements-dev.txt __pycache__ .mypy_cache .ruff_cache .pytest_cache
	@$(MAKE) setup_env
	@$(MAKE) install-lfs

# =============================
# 🧷 GIT LFS (CROSS-OS LOGIC)
# =============================

install-lfs:  ## Install Git LFS cross-platform
	@echo "📦 Checking for Git LFS..."
	@if command -v git-lfs >/dev/null 2>&1; then \
		echo "✅ Git LFS is already installed."; \
	else \
		echo "❌ Git LFS not found. Installing..."; \
		if [ "$(OS_NAME)" = "darwin" ]; then brew install git-lfs; \
		elif [ "$(OS_NAME)" = "linux" ]; then sudo apt-get install -y git-lfs || sudo dnf install -y git-lfs || sudo yum install -y git-lfs; \
		elif [ "$(OS_NAME)" = "windows_nt" ]; then choco install git-lfs -y; \
		else echo "⚠️ Please install Git LFS manually: https://git-lfs.github.com/"; exit 1; \
		fi; \
	fi
	@git lfs install || { echo '💥 Failed to initialize Git LFS'; exit 1; }
	@echo "🎉 Git LFS installed!"

# =============================
# 🧾 HELP
# =============================

help:  ## Show this help message
	@echo ""
	@echo "🛠️  Available Make targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================
# 🚀 FULL BOOTSTRAP
# =============================

bootstrap:  ## Bootstrap + commit + push current branch
	@echo "🚀 Bootstrapping project from scratch..."
	@$(MAKE) reinstall
	@echo "🔧 Installing pre-commit hooks..."
	@. $(VENV_ACTIVATE) && pre-commit install || echo "⚠️ Failed to install pre-commit hooks"
	@$(MAKE) check-code
	@git add -A
	@git commit -m "🤖 Auto-bootstrap update" || echo "⚠️ Nothing to commit."
	@git push origin $(CURRENT_BRANCH)
	@echo "✅ Bootstrap complete. Run: source $(VENV_ACTIVATE)"
