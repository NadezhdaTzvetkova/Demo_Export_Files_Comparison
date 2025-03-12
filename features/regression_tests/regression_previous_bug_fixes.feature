@regression_tests @previous_bugs @export_comparison
Feature: Validate previous bug fixes in export file processing
@regression_previous_bugs
Scenario: Ensure previous issues do not reappear
	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
12 I have a bank export file "bank_export_baseline_test.csv" from the new system
	When I run the export file comparison
	Then no previously resolved issues should reappear
