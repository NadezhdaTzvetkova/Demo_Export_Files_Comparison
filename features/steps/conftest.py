import os
import pytest
import logging
import allure
from _pytest.fixtures import FixtureRequest
from datetime import datetime

# ===================== SESSION LEVEL HOOKS =====================

def pytest_sessionstart(session):
    """Runs once before any tests start."""
    print("🛠 Running Gherkin indentation fix before test execution...")
    script_path = os.path.join("scripts", "fix_gherkin_indentation.py")

    try:
        result = os.system(f"python {script_path}")
        if result == 0:
            print("✅ Gherkin files formatted successfully.")
        else:
            print("❌ Error occurred while formatting Gherkin files.")
    except Exception as e:
        print(f"⚠️ Failed to run fix_gherkin_indentation.py: {e}")

    if any(tag in session.config.invocation_params.args for tag in ["regression", "performance"]):
        print("📂 Ensuring required large test files are available...")
        large_file_script = os.path.join("scripts", "download_large_files.py")
        try:
            result = os.system(f"python {large_file_script}")
            if result == 0:
                print("✅ Large files are ready.")
            else:
                print("❌ Error downloading large test files.")
        except Exception as e:
            print(f"⚠️ Failed to download large files: {e}")

def pytest_sessionfinish(session, exitstatus):
    """Runs once after all tests finish."""
    print("🎉 All tests completed!")

# ===================== BDD HOOKS =====================

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request: FixtureRequest, feature, scenario):
    """Hook that runs before each scenario."""
    print(f"📌 Starting scenario: {scenario.name}")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f"{scenario.name.replace(' ', '_').replace('/', '_')}.log"
    log_path = os.path.join(log_dir, log_filename)

    request.config._scenario_log_path = log_path
    with open(log_path, "w") as f:
        f.write(f"🧪 Starting scenario: {scenario.name}\n")

    allure.dynamic.title(scenario.name)
    for tag in scenario.tags:
        allure.dynamic.tag(tag)

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_scenario(request: FixtureRequest, feature, scenario):
    """Hook that runs after each scenario."""
    if scenario.status == "failed":
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"✅ Scenario passed: {scenario.name}")

    log_path = getattr(request.config, "_scenario_log_path", None)
    if log_path and os.path.exists(log_path):
        with open(log_path, "r") as f:
            content = f.read()
        allure.attach(content, name="Scenario Log", attachment_type=allure.attachment_type.TEXT)

# ===================== CUSTOM FEATURE LOGGING =====================

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_feature(request: FixtureRequest, feature):
    """Mimics Behave's before_feature."""
    print(f"🚀 Starting feature: {feature.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_feature(request: FixtureRequest, feature):
    """Mimics Behave's after_feature."""
    print(f"🏁 Completed feature: {feature.name}")
