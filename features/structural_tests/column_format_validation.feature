@structural_tests @column_format @export_comparison
Feature: Validate column format consistency
@column_format_check
Scenario Outline: Verify "<column>" format is consistent across exports
	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
12 I have a bank export file "bank_export_baseline_test.csv" from the new system
	When I check the format of "<column>"
	Then the format should be consistent in both files
Examples:
| column            |
| transaction_id    |
| account_number    |
| transaction_date  |
| customer_id       |
