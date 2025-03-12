@structural_tests @header_mismatch @export_comparison
Feature: Validate correct headers in export files
@header_mismatch_check
Scenario: Detect missing or incorrect headers
	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
		And I have a bank export file "bank_export_baseline_test.csv" from the new system
	When I check the file headers
	Then there should be no missing or incorrect headers
