Feature: Validate Decimal Precision Consistency
@decimal_precision @format_check
Scenario Outline: Ensure all monetary values follow correct decimal precision
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then all monetary values should have exactly two decimal places
		And values should not contain more than two decimal places
		And rounding inconsistencies should be flagged
Examples:
| file_name                              | sheet_name |
| bank_export_baseline_test.csv         | N/A        |
| bank_export_baseline_test.xlsx        | Sheet1     |
@decimal_precision @rounding_errors @edge_case
Scenario Outline: Detect incorrect decimal precision values
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then values with more than two decimal places should be flagged
		And rounding errors should be logged with suggested corrections
Examples:
| file_name                             | sheet_name |
| bank_export_decimal_precision_test.csv | N/A        |
| bank_export_decimal_precision_test.xlsx | Sheet1     |
@decimal_precision @large_transactions
Scenario Outline: Ensure large transactions maintain correct decimal precision
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then large transactions above $1,000,000 should have correctly formatted decimal precision
		And any rounding discrepancies should be reported
		And scientific notation should not be used
Examples:
| file_name                              | sheet_name |
| bank_export_large_transactions_test.csv | N/A        |
| bank_export_large_transactions_test.xlsx | Sheet1     |
@decimal_precision @negative_values
Scenario Outline: Ensure decimal precision is maintained for negative transactions
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then negative values should have consistent decimal precision
		And any discrepancies in negative amounts should be flagged
Examples:
| file_name                             | sheet_name |
| bank_export_negative_values_test.csv  | N/A        |
| bank_export_negative_values_test.xlsx | Sheet1     |
@decimal_precision @currency_conversion
Scenario Outline: Validate decimal precision for foreign currency conversions
	Given a bank export file "<file_name>"
	When I check the "Amount" and "Exchange Rate" columns in the "<sheet_name>" sheet
	Then converted values should maintain accurate decimal precision
		And rounding should be consistent with financial regulations
		And discrepancies should be logged for review
Examples:
| file_name                                 | sheet_name |
| bank_export_foreign_transactions_test.csv | N/A        |
| bank_export_foreign_transactions_test.xlsx| Sheet1     |
