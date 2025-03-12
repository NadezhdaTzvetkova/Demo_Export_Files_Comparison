@data_validation @delimiter_issues @export_comparison
Feature: Detect inconsistent delimiters in CSV files
@delimiter_check
Scenario: Identify incorrect or inconsistent delimiters in "bank_export_csv_inconsistent_delimiters_validation_params.csv"
	Given I have a CSV bank export file "bank_export_csv_inconsistent_delimiters_validation_params.csv"
	When I check the delimiter format
	Then the delimiter should be consistent throughout the file
