Feature: Validate Negative Values in Export Files
@negative_values @data_quality @transaction_validation
Scenario Outline: Ensure negative values are correctly recorded
	Given a bank export file "<file_name>"
	When I check for negative values in the "<sheet_name>" sheet
	Then negative values should only be present in debit transactions
		And credit transactions should not have negative values
		And incorrect negative values should be flagged for review
		And a correction suggestion should be provided
Examples:
| file_name                              | sheet_name |
| bank_export_baseline_test.csv         | N/A        |
| bank_export_baseline_test.xlsx        | Sheet1     |
@negative_values @edge_case @zero_amounts
Scenario Outline: Detect zero and negative transaction amounts
	Given a bank export file "<file_name>"
	When I check for negative and zero values in the "<sheet_name>" sheet
	Then negative amounts should only exist for debit transactions
		And zero amounts should be flagged as potential errors
		And transactions with zero values should be logged for further review
Examples:
| file_name                              | sheet_name |
| bank_export_negative_values_test.csv  | N/A        |
| bank_export_negative_values_test.xlsx | Sheet1     |
@negative_values @currency_conversion @data_consistency
Scenario Outline: Ensure negative values are correctly handled in currency conversions
	Given a bank export file "<file_name>"
	When I check the "Amount" and "Exchange Rate" columns in the "<sheet_name>" sheet
	Then converted values should maintain accurate negative value handling
		And rounding should be consistent with financial regulations
		And discrepancies should be logged for review
Examples:
| file_name                                 | sheet_name |
| bank_export_currency_conversion_test.csv | N/A        |
| bank_export_currency_conversion_test.xlsx| Sheet1     |
@negative_values @edge_case @large_files @performance
Scenario Outline: Validate negative values in large datasets
	Given a bank export file "<file_name>"
	When I check for negative values in a file with more than 100,000 rows
	Then all negative values should be correctly identified
		And system performance should be benchmarked for optimization
		And a detailed report should be generated with flagged transactions
Examples:
| file_name                               | sheet_name |
| bank_export_large_file_negative_values.csv | N/A        |
| bank_export_large_file_negative_values.xlsx | Sheet1     |
@negative_values @high_risk @fraud_detection
Scenario Outline: Detect suspicious negative values in high-risk transactions
	Given a bank export file "<file_name>"
	When I check for negative values in the "<sheet_name>" sheet
	Then high-risk transactions with excessive negative amounts should be flagged
		And unusual negative values should trigger an alert for fraud analysis
		And flagged transactions should be escalated for further investigation
Examples:
| file_name                                  | sheet_name |
| bank_export_high_risk_negative_values.csv  | N/A        |
| bank_export_high_risk_negative_values.xlsx | Sheet1     |
