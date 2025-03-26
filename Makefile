.PHONY: setup_env install test allure-report clean lock

# Command to create virtual environment, upgrade pip, install dependencies, and run setup_env.sh
setup_env:
	@echo "🚀 Setting up environment..."
	# Run the setup_env.sh script to create a virtual environment, upgrade pip, and install dependencies
	./setup_env.sh

# Command to install dependencies (in case you need to install them again)
install:
	@echo "📦 Installing dependencies..."
	# Install the dependencies while upgrading them to the latest version
	source .venv/bin/activate && pip install --upgrade -r requirements.txt

# Run BDD tests (all or by tag) using behave-parallel
test:
	@echo "🧪 Running BDD tests in parallel with behave-parallel"
	# Run the tests using the behave-parallel tool
	source .venv/bin/activate && behave-parallel -n 4 -f allure_behave.formatter:AllureFormatter -o allure-results/behave $(TAGS)

# Generate Allure HTML report
allure-report:
	@echo "📊 Generating Allure report..."
	# Generate the Allure report from the test results
	source .venv/bin/activate && allure generate allure-results/behave --clean -o allure-report
	@echo "✅ Allure report generated at: allure-report/index.html"

# Clean up old results and reports
clean:
	@echo "🧹 Cleaning old results and reports..."
	# Remove old files and directories such as results, reports, and virtual environments
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml requirements.txt requirements.lock .venv

# Regenerate requirements.lock from requirements.txt and requirements-vcs.in
lock:
	@echo "🔒 Regenerating requirements.lock..."
	# Regenerate the requirements.lock file to lock dependencies for the project
	source .venv/bin/activate && pip-compile --output-file=requirements.lock requirements.txt requirements-vcs.in
