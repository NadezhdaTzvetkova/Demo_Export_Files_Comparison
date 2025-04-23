.PHONY: \
	setup setup_env check_venv check-env \
	install install-dev lock upgrade \
	test allure-report \
	format lint check-style \
	clean security-audit reinstall

# =============================
# 🔍 PLATFORM DETECTION
# =============================

OS_NAME := $(shell uname | tr '[:upper:]' '[:lower:]')
PYTHON := python3

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
	@echo "📦 Installing pip-tools..."
	@. $(VENV_ACTIVATE) && pip install pip-tools
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
	@./.setup_env.sh

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
# 🎨 CODE FORMATTING & LINTING
# =============================

format:
	@echo "🎨 Formatting code with black and ruff..."
	@. $(VENV_ACTIVATE) && black .
	@. $(VENV_ACTIVATE) && ruff check . --fix
	@echo "✅ Code formatted!"

lint:
	@echo "🔍 Running ruff lint checks (non-fixing)..."
	@. $(VENV_ACTIVATE) && ruff check .
	@echo "✅ Linting completed!"

check-style:
	@echo "🔎 Checking code style (ruff lint + ruff format --check)..."
	@. $(VENV_ACTIVATE) && ruff check .
	@. $(VENV_ACTIVATE) && ruff format --check .
	@echo "✅ Style check passed (no issues found)!"

# =============================
# 🧹 CLEANUP & SECURITY
# =============================

clean:
	@echo "🧹 Cleaning up project artifacts..."
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml .venv *.lock

security-audit:
	@echo "🛡️  Running pip-audit for security vulnerabilities..."
	@. $(VENV_ACTIVATE) && pip install pip-audit >/dev/null
	@. $(VENV_ACTIVATE) && pip-audit || echo "⚠️  Vulnerabilities detected. Review above."

# =============================
# ♻️ FULL REINSTALL
# =============================

reinstall:
	@echo "💣 Removing .venv, lock files and caches..."
	rm -rf .venv requirements.txt requirements-dev.txt __pycache__ .mypy_cache .ruff_cache .pytest_cache
	@echo "🔁 Re-running setup..."
	./.setup_env.sh
