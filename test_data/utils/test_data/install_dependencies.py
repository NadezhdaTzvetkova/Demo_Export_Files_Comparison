import subprocess
import sys
import os

def get_project_root():
    """Return the root directory of the project."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# List of required dependencies
dependencies = [
    "behave",
    "pandas",
    "openpyxl",
    "pyarrow", # or "pyarrow pandas" | pip install pyarrow pandas
    "pytest",
    "xlrd",
    "chardet"
]

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], cwd=get_project_root())
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}. Error: {e}")
        sys.exit(1)

def check_and_install_dependencies():
    """Check if each dependency is installed and install it if missing."""
    for package in dependencies:
        try:
            __import__(package)
            print(f"✅ {package} is already installed.")
        except ImportError:
            print(f"⚠️ {package} not found. Installing...")
            install_package(package)
            print(f"✅ {package} installed successfully.")

if __name__ == "__main__":
    check_and_install_dependencies()
