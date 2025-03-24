# Makefile for BDD Automation

.PHONY: test allure-report clean lock

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
	rm -rf allure-results allure-report .pytest_cache .coverage coverage.xml

# Regenerate requirements.lock
lock:
	pip-compile --output-file=requirements.lock requirements.txt
