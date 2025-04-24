.PHONY: \
	setup setup_env check_venv check-env \
	install install-dev lock upgrade \
	test allure-report \
	format lint check-style check-code \
	type-check pre-commit-run \
	clean security-audit reinstall \
	install-lfs bootstrap

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

check_venv:
	@echo "🔍 Checking if a virtual environment is already active..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "⚠️  Active virtualenv detected: $$VIRTUAL_ENV"; \
		echo "❌ Please deactivate it before running this script."; \
		exit 1; \
	else \
		echo "✅ No active virtualenv detected."; \
	fi

setup_env: check_venv
	@echo "🚀 Creating virtual environment in .venv..."
	@test -d .venv || $(PYTHON) -m venv .venv
	@echo "⬆️  Upgrading pip..."
	@. $(VENV_ACTIVATE) && pip install --upgrade pip
	@echo "📦 Installing pip-tools and pre-commit..."
	@. $(VENV_ACTIVATE) && pip install pip-tools pre-commit
	@echo "✅ Setup complete. Run: source $(VENV_ACTIVATE)"

check-env:
	@echo "🔍 Checking .venv and Python version..."
	@if [ ! -d ".venv" ]; then \
		echo "❌ .venv not found. Please run: make setup_env"; \
		exit 1; \
	fi
	@echo "✅ .venv exists."
	@echo "🐍 Validating Python version..."
	@. $(VENV_ACTIVATE) && $(VENV_PYTHON) --version | grep '3.11' >/dev/null || \
		(echo '❌ Python is not 3.11.x' && exit 1)

setup:
	@echo "⚙️ Running environment setup..."
	@./.setup_env.sh || echo "⚠️ .setup_env.sh missing or failed"
	@$(MAKE) install-lfs

# =============================
# 📦 DEPENDENCY MANAGEMENT
# =============================

install:
	@echo "📦 Installing runtime dependencies..."
	@. $(VENV_ACTIVATE) && pip install -r requirements.txt

install-dev:
	@echo "🔧 Installing dev dependencies..."
	@. $(VENV_ACTIVATE) && pip install -r requirements-dev.txt

lock:
	@echo "🔒 Locking runtime and dev dependencies..."
	@. $(VENV_ACTIVATE) && pip-compile --output-file=requirements.txt requirements.in
	@. $(VENV_ACTIVATE) && pip-compile --output-file=requirements-dev.txt requirements-dev.in

upgrade:
	@echo "⬆️  Upgrading requirements and locking them..."
	@. $(VENV_ACTIVATE) && pip-compile --upgrade --output-file=requirements.txt requirements.in
	@. $(VENV_ACTIVATE) && pip-compile --upgrade --output-file=requirements-dev.txt requirements-dev.in
	@echo "✅ Dependencies upgraded and locked."

# =============================
# 🧪 TESTING & REPORTING
# =============================

test:
	@echo "🧪 Running BDD tests with behave-parallel..."
	@. $(VENV_ACTIVATE) && behave-parallel -n 4 -f allure_behave.formatter:AllureFormatter -o allure-results/behave $(TAGS)

allure-report:
	@echo "📊 Generating Allure report..."
	@. $(VENV_ACTIVATE) && allure generate allure-results/behave --clean -o allure-report
	@echo "✅ Report at: allure-report/index.html"

# =============================
# 🎨 CODE CHECKS (NON-BLOCKING)
# =============================

format:
	@echo "🎨 Formatting code (black + ruff)..."
	@. $(VENV_ACTIVATE) && black . || true
	@. $(VENV_ACTIVATE) && ruff check . --fix || true

lint:
	@echo "🔍 Running ruff lint checks..."
	@. $(VENV_ACTIVATE) && ruff check . || true

check-style:
	@echo "🔎 Checking code style (non-blocking)..."
	@. $(VENV_ACTIVATE) && ruff check . || true
	@. $(VENV_ACTIVATE) && ruff format --check . || true

type-check:
	@echo "📦 Running mypy type checks (non-blocking)..."
	@. $(VENV_ACTIVATE) && mypy . || true

pre-commit-run:
	@echo "🧼 Running pre-commit on all files (non-blocking)..."
	@. $(VENV_ACTIVATE) && pre-commit run --all-files || true

check-code:
	@echo "🛠️ Running all code checks (non-blocking)..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) type-check

# =============================
# 🧹 CLEANUP & SECURITY
# =============================

clean:
	@echo "🧹 Cleaning up temporary files..."
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml .venv *.lock

security-audit:
	@echo "🛡️ Running pip-audit (non-blocking)..."
	@. $(VENV_ACTIVATE) && pip install pip-audit >/dev/null
	@. $(VENV_ACTIVATE) && pip-audit || echo "⚠️ Vulnerabilities found."

# =============================
# ♻️ FULL REINSTALL
# =============================

reinstall:
	@echo "💣 Reinstalling environment and dependencies..."
	rm -rf .venv requirements.txt requirements-dev.txt __pycache__ .mypy_cache .ruff_cache .pytest_cache
	@$(MAKE) setup_env
	@$(MAKE) install-lfs

# =============================
# 🧷 GIT LFS (Cross-OS Logic)
# =============================

install-lfs:
	@echo "📦 Ensuring Git LFS is installed..."
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
	@echo "🎉 Git LFS ready to use."

# =============================
# 🚀 FULL BOOTSTRAP
# =============================

bootstrap:
	@echo "🚀 Bootstrapping full environment..."
	@$(MAKE) reinstall
	@echo "🔧 Installing pre-commit hooks..."
	@. $(VENV_ACTIVATE) && pre-commit install || echo "⚠️ Failed to install pre-commit hooks"
	@$(MAKE) check-code
	@git add -A
	@git commit -m "🤖 Auto-bootstrap update" || echo "⚠️ Nothing to commit."
	@git push origin $(CURRENT_BRANCH)
	@echo "✅ Bootstrap complete. Run: source $(VENV_ACTIVATE)"
