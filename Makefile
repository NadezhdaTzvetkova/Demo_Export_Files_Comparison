.PHONY: \
	setup setup_env check_venv check-env \
	install install-dev lock upgrade \
	test allure-report \
	format lint check-style \
	clean security-audit reinstall \
	install-lfs

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
# 🎨 CODE FORMATTING & LINTING
# =============================

format:
	@echo "🎨 Formatting code with black and ruff..."
	@. $(VENV_ACTIVATE) && black .
	@. $(VENV_ACTIVATE) && ruff check . --fix
	@echo "✅ Code formatted!"

lint:
	@echo "🔍 Running ruff lint checks..."
	@. $(VENV_ACTIVATE) && ruff check .
	@echo "✅ Linting completed!"

check-style:
	@echo "🔎 Checking code style (ruff lint + ruff format --check)..."
	@. $(VENV_ACTIVATE) && ruff check .
	@. $(VENV_ACTIVATE) && ruff format --check .
	@echo "✅ Style check passed!"

# =============================
# 🧹 CLEANUP & SECURITY
# =============================

clean:
	@echo "🧹 Cleaning up project artifacts..."
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml .venv *.lock

security-audit:
	@echo "🛡️  Running pip-audit..."
	@. $(VENV_ACTIVATE) && pip install pip-audit >/dev/null
	@. $(VENV_ACTIVATE) && pip-audit || echo "⚠️ Vulnerabilities found."

# =============================
# ♻️ FULL REINSTALL
# =============================

reinstall:
	@echo "💣 Wiping environment and caches..."
	rm -rf .venv requirements.txt requirements-dev.txt __pycache__ .mypy_cache .ruff_cache .pytest_cache
	@echo "🔁 Reinstalling environment..."
	@$(MAKE) setup_env
	@$(MAKE) install-lfs

# =============================
# 🧷 GIT LFS (Cross-OS Logic)
# =============================

install-lfs:
	@echo "📦 Checking for Git LFS..."
	@if command -v git-lfs >/dev/null 2>&1; then \
		echo "✅ Git LFS is already installed."; \
	else \
		echo "❌ Git LFS not found."; \
		if [ "$(OS_NAME)" = "darwin" ]; then \
			echo "🍏 Installing Git LFS on macOS..."; \
			if ! command -v brew >/dev/null 2>&1; then \
				echo "📥 Installing Homebrew..."; \
				/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; \
			fi; \
			brew install git-lfs; \
		elif [ "$(OS_NAME)" = "linux" ]; then \
			echo "🐧 Installing Git LFS on Linux..."; \
			if command -v apt-get >/dev/null 2>&1; then \
				sudo apt-get update && sudo apt-get install -y git-lfs; \
			elif command -v dnf >/dev/null 2>&1; then \
				sudo dnf install -y git-lfs; \
			elif command -v yum >/dev/null 2>&1; then \
				sudo yum install -y git-lfs; \
			else \
				echo "⚠️ Unsupported package manager. Please install Git LFS manually: https://git-lfs.github.com/"; \
				exit 1; \
			fi; \
		elif [ "$(OS_NAME)" = "windows_nt" ]; then \
			echo "🪟 Installing Git LFS on Windows..."; \
			if command -v choco >/dev/null 2>&1; then \
				choco install git-lfs -y; \
			else \
				echo "⚠️ Chocolatey not found. Please install Git LFS manually: https://git-lfs.github.com/"; \
				exit 1; \
			fi; \
		else \
			echo "❌ Unsupported OS: $(OS_NAME). Install Git LFS manually."; \
			exit 1; \
		fi; \
	fi
	@git lfs install || { echo '💥 Failed to initialize Git LFS'; exit 1; }
	@echo "🎉 Git LFS installed and ready to use!"
