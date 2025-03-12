@data_validation @encoding @export_comparison
Feature: Validate file encoding consistency in export files

Description: Validate that both export files from the old and new systems are encoded in UTF-8.
@encoding_match
Scenario: Ensure both export files use UTF-8 encoding
	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
		And I have a bank export file "bank_export_baseline_test.csv" from the new system
	When I check the file encoding
	Then both files should be encoded in UTF-8
