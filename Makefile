# Makefile for BDD Automation

.PHONY: test allure-report clean install lock

# Install dependencies (compile requirements.txt and install packages)
install:
	@echo "📦 Installing dependencies..."
	# Compile requirements.txt from requirements.in if not exists or outdated
	@if [ ! -f requirements.txt ] || [ requirements.in -nt requirements.txt ]; then \
		pip-compile requirements.in --output-file=requirements.txt; \
	fi
	# Install the dependencies
	pip install -r requirements.txt

# Run BDD tests (all or by tag) using behave-parallel
test:
	@echo "🧪 Running BDD tests in parallel with behave-parallel"
	behave-parallel -n 4 -f allure_behave.formatter:AllureFormatter -o allure-results/behave $(TAGS)

# Generate Allure HTML report
allure-report:
	@echo "📊 Generating Allure report..."
	allure generate allure-results/behave --clean -o allure-report
	@echo "✅ Allure report generated at: allure-report/index.html"

# Clean up old results and reports
clean:
	@echo "🧹 Cleaning old results and reports..."
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml requirements.txt requirements.lock

# Regenerate requirements.lock from requirements.txt and requirements-vcs.in
lock:
	@echo "🔒 Regenerating requirements.lock..."
	pip-compile --output-file=requirements.lock requirements.txt requirements-vcs.in
