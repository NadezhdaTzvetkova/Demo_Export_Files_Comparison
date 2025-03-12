import os
import sys
import subprocess


def get_project_root():
    """Return the root directory of the project."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def run_command(command):
    """Run a shell command and check for errors."""
    print(f"🛠️ Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=get_project_root())

    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        print(f"Error output:\n{result.stderr}")
        exit(result.returncode)
    else:
        print(f"✅ Command succeeded: {command}")
        print(f"Output:\n{result.stdout}")


# Define available test suites
TEST_SUITES = {
    "all": "--tags=export_comparison",
    "data_validation": "--tags=data_validation",
    "performance": "--tags=performance_tests",
    "regression": "--tags=regression_tests"
}


def run_tests(suite):
    """Runs the specified test suite with Allure reporting."""
    if suite not in TEST_SUITES:
        print(f"❌ Invalid suite '{suite}'. Choose from: {list(TEST_SUITES.keys())}")
        sys.exit(1)

    print(f"🚀 Running test suite: {suite}")

    # Run Behave with the selected suite and generate Allure reports
    cmd = f"behave {TEST_SUITES[suite]} --format=allure_behave.formatter:AllureFormatter -o reports/allure_results"
    run_command(cmd)

    print("📊 Generating Allure report...")
    run_command("allure generate reports/allure_results -o reports/allure_report --clean")

    print("🔍 Opening Allure report...")
    run_command("allure open reports/allure_report")

    print("✅ Test execution completed!")


if __name__ == "__main__":
    print("📦 Installing dependencies...")
    run_command("python utils/install_dependencies.py")

    if len(sys.argv) < 2:
        print("⚠️ Usage: python run_tests.py <suite>")
        print(f"Available suites: {list(TEST_SUITES.keys())}")
        sys.exit(1)

    suite_name = sys.argv[1]
    run_tests(suite_name)
