@data_validation @date_format @export_comparison
Feature: Validate date format consistency in export files
@date_format_check
Scenario Outline: Verify "<date_column>" format follows "YYYY-MM-DD"
	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
		And I have a bank export file "bank_export_baseline_test.csv" from the new system
	When I check the format of "<date_column>"
	Then all values should follow "YYYY-MM-DD"
Examples:
| date_column        |
| transaction_date   |
| posting_date       |
| settlement_date    |
