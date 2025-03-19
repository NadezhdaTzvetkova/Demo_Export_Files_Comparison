# features/environment.py
import os
import subprocess


def before_all(context):
    """Hook to run before all tests start."""
    print("🔧 Initializing test environment...")

    # Define delimiter mapping for feature tests
    context.delimiter_mapping = {
        "comma": ",",
        "semicolon": ";",
        "TAB": "\t",
        "pipe": "|"
    }

    # Ensure large test files are available for regression and performance tests
    if "regression" in context.config.tags or "performance" in context.config.tags:
        print("📂 Ensuring required large test files are available...")
        script_path = os.path.join("scripts", "download_large_files.py")

        try:
            result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
            print(result.stdout)  # Show output of the script execution
            print("✅ Large files are ready.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error downloading files: {e.stderr}")


def before_feature(context, feature):
    """Hook to run before each feature."""
    print(f"\n🚀 Starting feature: {feature.name}")
    context.current_feature = feature.name  # Track current feature


def before_scenario(context, scenario):
    """Hook to run before each scenario."""
    print(f"\n📌 Starting scenario: {scenario.name}")
    context.current_scenario = scenario.name  # Track current scenario


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
    print("\n🎉 All tests completed successfully!")
