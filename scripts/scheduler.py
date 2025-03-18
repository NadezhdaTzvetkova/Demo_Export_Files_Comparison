from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import time
import requests

GITHUB_TOKEN = "your_personal_access_token"  # Replace with your GitHub token
GITHUB_REPO = "NadezhdaTzvetkova/Demo_Export_Files_Comparison"
GITHUB_WORKFLOW = "test_execution.yml"

def run_tests_locally():
    """Runs tests locally with Allure reporting."""
    print("🚀 Running scheduled test execution locally...")

    # Run Behave with Allure
    command = "python run_tests.py all"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Log output
    with open("reports/daily_test_log.txt", "a") as log_file:
        log_file.write("\n=== Local Test Execution Log ===\n")
        log_file.write(result.stdout)
        log_file.write("\n=== End of Log ===\n")

    if result.returncode != 0:
        print("❌ Local test execution failed. Check logs.")
    else:
        print("✅ Local tests completed successfully.")

def trigger_github_action():
    """Triggers the GitHub Actions workflow remotely."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{GITHUB_WORKFLOW}/dispatches"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    data = {"ref": "main"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print("✅ GitHub Actions workflow triggered successfully!")
    else:
        print(f"❌ Failed to trigger GitHub Actions: {response.text}")

# Schedule the job
scheduler = BackgroundScheduler()
scheduler.add_job(run_tests_locally, 'cron', hour=9, minute=0)  # Runs daily at 9:00 AM
scheduler.add_job(trigger_github_action, 'cron', hour=12, minute=0)  # Runs GitHub Actions at 12:00 PM

scheduler.start()
print("📅 Test Scheduler is running (Local + GitHub Actions). Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(3600)  # Keep the script running
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("❌ Scheduler stopped.")
