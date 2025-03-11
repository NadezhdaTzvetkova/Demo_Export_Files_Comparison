import subprocess
import os


def get_project_root():
    """Return the root directory of the project."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def run_command(command):
    """Run a shell command and check for errors."""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=get_project_root())

    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        print(f"Error output: {result.stderr}")
        exit(result.returncode)
    else:
        print(f"✅ Command succeeded: {command}")
        print(f"Output: {result.stdout}")


if __name__ == "__main__":
    print("📦 Installing dependencies...")
    run_command("python utils/install_dependencies.py")

    print("🚀 Running Behave tests...")
    run_command("behave")
