# features/environment.py

import os
import subprocess
import allure


def before_all(context):
    """Hook to run before all tests start. Ensures formatting and test data setup."""
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

    # Handle performance or regression test data setup
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

    # Prepare log path per scenario
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    log_filename = f"{scenario.name.replace(' ', '_').replace('/', '_')}.log"
    log_path = os.path.join(logs_dir, log_filename)

    # Save the path for access in steps or after hooks
    context.log_path = log_path

    with open(log_path, "w") as log_file:
        log_file.write(f"🧪 Starting scenario: {scenario.name}\n")

    # Allure metadata: name + tags
    allure.dynamic.title(scenario.name)
    if scenario.tags:
        for tag in scenario.tags:
            allure.dynamic.tag(tag)


def after_scenario(context, scenario):
    """Hook to run after each scenario."""
    if scenario.status == "failed":
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"✅ Scenario passed: {scenario.name}")

    # Automatically attach log to Allure report
    if hasattr(context, "log_path") and os.path.exists(context.log_path):
        with open(context.log_path, "r") as log_file:
            log_content = log_file.read()
        allure.attach(log_content, name="Scenario Log", attachment_type=allure.attachment_type.TEXT)


def after_feature(context, feature):
    """Hook to run after each feature."""
    print(f"🏁 Completed feature: {feature.name}")


def after_all(context):
    """Hook to run after all tests complete."""
    print("🎉 All tests completed!")
