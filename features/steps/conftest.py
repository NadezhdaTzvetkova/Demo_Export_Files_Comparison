# ===================== conftest.py =====================
# This file contains hooks and configurations for the Pytest framework, specifically for integrating
# BDD with pytest-bdd and managing logging and file handling during test execution.
# It includes hooks for:
# - Managing session-level tasks like fixing Gherkin indentation and ensuring large test files for regression/performance.
# - Handling scenario-level logging and acquiring file locks to prevent conflicts in parallel execution.
# - Mimicking Behave's `before_feature` and `after_feature` hooks for feature-level logging.
#
# Purpose:
# - Organize logging and file handling.
# - Set up and tear down specific behaviors for BDD scenarios and features.
# - Ensure smooth execution of regression and performance tests with retries for file downloads.

import os
import pytest
import allure
from _pytest.fixtures import FixtureRequest
from filelock import FileLock
import logging
from logging.handlers import RotatingFileHandler
import time
import random

# ===================== SESSION LEVEL HOOKS =====================


def pytest_sessionstart(session):
    """Runs once before any tests start.
    This hook is used to:
    - Fix Gherkin file indentation.
    - Ensure large test files are available for regression/performance testing.
    """
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

    # Ensure required large test files are available if regression or performance tests are being executed
    if any(
        tag in session.config.invocation_params.args
        for tag in ["regression", "performance"]
    ):
        print("📂 Ensuring required large test files are available...")
        large_file_script = os.path.join("scripts", "download_large_files.py")
        attempt = 0
        max_retries = 3  # Retry up to 3 times if download fails
        while attempt < max_retries:
            try:
                result = os.system(f"python {large_file_script}")
                if result == 0:
                    print("✅ Large files are ready.")
                    break
                else:
                    print("❌ Error downloading large test files.")
            except Exception as e:
                print(f"⚠️ Failed to download large files: {e}")
            attempt += 1
            if attempt < max_retries:
                wait_time = random.randint(5, 15)  # Random wait time between retries
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)


def pytest_sessionfinish(session, exitstatus):
    """Runs once after all tests finish.
    Here, you can add performance metrics collection if required after all tests are executed.
    """
    print("🎉 All tests completed!")


# ===================== BDD HOOKS =====================


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request: FixtureRequest, feature, scenario):
    """This hook runs before each scenario starts.
    - Sets up logging for the scenario.
    - Acquires a file lock to avoid parallel I/O conflicts.
    """
    print(f"📌 Starting scenario: {scenario.name}")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f"{scenario.name.replace(' ', '_').replace('/', '_')}.log"
    log_path = os.path.join(log_dir, log_filename)

    # Save the log path in request.config for use in after hooks
    request.config._scenario_log_path = log_path
    with open(log_path, "w") as f:
        f.write(f"🧪 Starting scenario: {scenario.name}\n")

    # Set up a rotating file handler to manage the log file size
    log_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=3)
    log_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(log_handler)

    # Log the start of the scenario
    logging.info(f"Starting scenario: {scenario.name}")

    # Attach feature tags to the Allure report
    allure.dynamic.title(scenario.name)
    for tag in scenario.tags:
        allure.dynamic.tag(tag)

    # Lock the file for the scenario to avoid parallel file write conflicts
    context = request.node._request.getfixturevalue("context")
    context.file_lock = FileLock(f"{scenario.name.replace(' ', '_')}.lock")
    context.file_lock.acquire(timeout=10)  # Timeout after 10 seconds


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_scenario(request: FixtureRequest, feature, scenario):
    """This hook runs after each scenario finishes.
    - Logs the result (pass/fail) and attaches the log to the Allure report.
    - Releases the file lock after the scenario.
    """
    if scenario.status == "failed":
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"✅ Scenario passed: {scenario.name}")

    log_path = getattr(request.config, "_scenario_log_path", None)
    if log_path and os.path.exists(log_path):
        with open(log_path, "r") as f:
            content = f.read()
        allure.attach(
            content, name="Scenario Log", attachment_type=allure.attachment_type.TEXT
        )

    # Release the lock after the scenario is done
    context = request.node._request.getfixturevalue("context")
    if hasattr(context, "file_lock"):
        context.file_lock.release()


# ===================== CUSTOM FEATURE LOGGING =====================


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_feature(request: FixtureRequest, feature):
    """This hook mimics Behave's before_feature.
    - Logs the start of each feature.
    """
    print(f"🚀 Starting feature: {feature.name}")


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_feature(request: FixtureRequest, feature):
    """This hook mimics Behave's after_feature.
    - Logs the completion of each feature.
    """
    print(f"🏁 Completed feature: {feature.name}")
