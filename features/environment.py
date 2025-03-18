# features/environment.py
import subprocess
import os

def before_all(context):
    """Hook to run before all tests start."""
    if "regression" in context.config.tags or "performance" in context.config.tags:
        print("📂 Ensuring required large test files are available...")
        script_path = os.path.join("scripts", "download_large_files.py")
        result = subprocess.run(["python", script_path], check=True)
        if result.returncode == 0:
            print("✅ Large files are ready.")
        else:
            print("❌ Error downloading files.")

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
