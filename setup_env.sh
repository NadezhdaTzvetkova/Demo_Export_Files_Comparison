#!/bin/bash

echo "🛠️ Setting up the Python development environment..."

# 1. Detect OS type
OS_TYPE="$(uname -s)"
case "${OS_TYPE}" in
    Linux*)     MACHINE=Linux ;;
    Darwin*)    MACHINE=Mac ;;
    CYGWIN*|MINGW*|MSYS*) MACHINE=Windows ;;
    *)          MACHINE="UNKNOWN:${OS_TYPE}" ;;
esac

echo "📦 Detected OS: ${MACHINE}"

# 2. Prevent stacking virtual environments
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "⚠️  A virtual environment is already active: $VIRTUAL_ENV"
    echo "❌ Please deactivate it before running this script."
    exit 1
fi

# 3. Ensure Python 3.11 is installed
if ! command -v python3.11 &>/dev/null; then
    echo "❌ Python 3.11 is not installed or not in PATH."
    echo "👉 Install it with: brew install python@3.11"
    exit 1
fi

# 4. Create virtual environment using Python 3.11
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment with Python 3.11..."
    python3.11 -m venv .venv
else
    echo "✅ Virtual environment already exists. Verifying version..."
    VENV_PYTHON_VERSION=$(.venv/bin/python --version 2>&1)
    if [[ "$VENV_PYTHON_VERSION" != *"3.11."* ]]; then
        echo "❌ Existing virtual environment is not using Python 3.11: $VENV_PYTHON_VERSION"
        echo "🧹 Please delete .venv and re-run this script."
        exit 1
    fi
fi

# 5. Upgrade pip
echo "⬆️  Upgrading pip..."
.venv/bin/pip install --upgrade pip

# 6. Install pip-tools
echo "🔧 Installing pip-tools..."
.venv/bin/pip install --upgrade pip-tools

# 7. Install runtime dependencies with fallback logic for pandas
if [ -f "requirements.txt" ]; then
    echo "📚 Installing requirements.txt..."
    if ! .venv/bin/pip install -r requirements.txt; then
        echo "⚠️ Initial install failed. Trying pandas fallback logic..."

        echo "➕ Installing numpy (build-time dep for pandas)..."
        .venv/bin/pip install "numpy<1.24" --no-build-isolation

        echo "➕ Installing Cython (pinned for compatibility)..."
        .venv/bin/pip install "Cython==0.29.36"

        echo "🔁 Retrying full install of requirements.txt..."
        .venv/bin/pip install -r requirements.txt
    fi
fi

# 8. Install dev dependencies
if [ -f "requirements-dev.txt" ]; then
    echo "🧪 Installing requirements-dev.txt..."
    .venv/bin/pip install -r requirements-dev.txt
fi

# 9. Set up pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔗 Installing pre-commit hooks..."
    .venv/bin/pip install pre-commit
    .venv/bin/pre-commit install
fi

# 10. Lock and re-install
echo "🔒 Running make lock to recompile requirements..."
make lock

echo "📦 Running make install-dev to finalize dev environment..."
make install-dev

echo ""
echo "✅ Setup complete."
echo "👉 To activate your environment, run:"
echo "   source .venv/bin/activate"
