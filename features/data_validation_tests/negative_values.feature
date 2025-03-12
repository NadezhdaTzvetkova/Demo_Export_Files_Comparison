@data_validation @negative_values @export_comparison
Feature: Validate handling of negative values in export files
@negative_values_check
Scenario Outline: Ensure "<numeric_column>" handles negative values correctly in "bank_export_negative_values_test.xlsx" and "bank_export_negative_values_test.csv"
	Given I have a bank export file "bank_export_negative_values_test.xlsx" from the old system
		And I have a bank export file "bank_export_negative_values_test.csv" from the new system
	When I compare the "<numeric_column>" column
	Then negative values should be processed correctly
Examples:
| numeric_column      |
| transaction_amount  |
| account_balance     |
| overdraft_limit     |
