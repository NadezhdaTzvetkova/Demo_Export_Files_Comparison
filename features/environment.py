import os
import subprocess


def before_all(context):
    """Hook to run before all tests start. Ensures Gherkin files are properly formatted."""

    print("🛠 Running Gherkin indentation fix before test execution...")
    script_path = os.path.join("scripts", "fix_gherkin_indentation.py")

    try:
        result = subprocess.run(["python", script_path], check=True)
        if result.returncode == 0:
            print("✅ Gherkin files formatted successfully.")
        else:
            print("❌ Error occurred while formatting Gherkin files.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to run fix_gherkin_indentation.py: {e}")

    # Check if test suite includes regression or performance tests
    if "regression" in context.config.tags or "performance" in context.config.tags:
        print("📂 Ensuring required large test files are available...")
        large_file_script = os.path.join("scripts", "download_large_files.py")

        try:
            result = subprocess.run(["python", large_file_script], check=True)
            if result.returncode == 0:
                print("✅ Large files are ready.")
            else:
                print("❌ Error downloading large test files.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to download large files: {e}")


def before_feature(context, feature):
    """Hook to run before each feature."""
    print(f"🚀 Starting feature: {feature.name}")


def before_scenario(context, scenario):
    """Hook to run before each scenario."""
    print(f"📌 Starting scenario: {scenario.name}")


def after_scenario(context, scenario):
    """Hook to run after each scenario."""
    if scenario.status == "failed":
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"✅ Scenario passed: {scenario.name}")


def after_feature(context, feature):
    """Hook to run after each feature."""
    print(f"🏁 Completed feature: {feature.name}")


def after_all(context):
    """Hook to run after all tests complete."""
    print("🎉 All tests completed!")
