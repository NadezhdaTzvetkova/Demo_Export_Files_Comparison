#!/usr/bin/env bash

set -e

echo "🛠️ Setting up the Python 3.11 environment..."

# 1. Detect OS
OS_TYPE="$(uname -s)"
case "${OS_TYPE}" in
    Linux*)     PLATFORM=Linux ;;
    Darwin*)    PLATFORM=Mac ;;
    CYGWIN*|MINGW*|MSYS*) PLATFORM=Windows ;;
    *)          PLATFORM="UNKNOWN:${OS_TYPE}" ;;
esac
echo "📦 Detected OS: ${PLATFORM}"

# 2. Prevent active virtual environments
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "⚠️  An active virtual environment is already running: $VIRTUAL_ENV"
    echo "❌ Please deactivate it first."
    exit 1
fi

# 3. Check Python 3.11
PYTHON=$(command -v python3.11 || true)
if [[ -z "$PYTHON" ]]; then
    echo "❌ Python 3.11 is not installed or not in PATH."
    if [[ "$PLATFORM" == "Mac" ]]; then
        echo "👉 Run: brew install python@3.11"
    else
        echo "👉 Install Python 3.11 manually and try again."
    fi
    exit 1
fi

# 4. Create .venv if missing
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment with Python 3.11..."
    $PYTHON -m venv .venv
else
    VENV_PYTHON_VERSION=$(.venv/bin/python --version 2>&1)
    if [[ "$VENV_PYTHON_VERSION" != *"3.11."* ]]; then
        echo "❌ .venv exists but is not using Python 3.11: $VENV_PYTHON_VERSION"
        echo "🧹 Please delete .venv and re-run this script."
        exit 1
    fi
    echo "✅ .venv already exists and uses Python 3.11"
fi

# 5. Upgrade pip
echo "⬆️  Upgrading pip..."
. .venv/bin/activate && pip install --upgrade pip

# 6. Install pip-tools
echo "🔧 Installing pip-tools..."
. .venv/bin/activate && pip install --upgrade pip-tools

# 7. Install runtime dependencies with pandas fallback
if [ -f "requirements.txt" ]; then
    echo "📚 Installing requirements.txt..."
    if ! .venv/bin/pip install -r requirements.txt; then
        echo "⚠️ First install failed. Applying fallback for pandas..."
        .venv/bin/pip install "numpy<1.24" "Cython==0.29.36" --no-build-isolation
        .venv/bin/pip install -r requirements.txt
    fi
fi

# 8. Install dev dependencies
if [ -f "requirements-dev.txt" ]; then
    echo "🧪 Installing requirements-dev.txt..."
    .venv/bin/pip install -r requirements-dev.txt
fi

# 9. Install pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔗 Setting up pre-commit hooks..."
    .venv/bin/pip install pre-commit
    .venv/bin/pre-commit install
fi

# 10. Lock & recompile
echo "🔒 Recompiling requirements..."
make lock

echo "📦 Finalizing dev install..."
make install-dev

echo ""
echo "✅ Setup complete."
echo "👉 To activate: source .venv/bin/activate"
