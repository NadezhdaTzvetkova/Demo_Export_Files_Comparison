Feature: Validate Whitespace Handling in Export Files
@whitespace_handling @data_quality @field_validation
Scenario Outline: Ensure fields do not contain leading or trailing spaces
	Given a bank export file "<file_name>"
	When I check for whitespace issues in the "<column_name>" column in the "<sheet_name>" sheet
	Then leading and trailing spaces should be removed from all text fields
		And fields with excessive whitespace should be flagged
		And a correction suggestion should be provided
Examples:
| file_name                              | sheet_name | column_name     |
| bank_export_baseline_test.csv         | N/A        | Description     |
| bank_export_baseline_test.xlsx        | Sheet1     | Description     |
@whitespace_handling @account_numbers @edge_case
Scenario Outline: Detect leading or trailing spaces in account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then account numbers should not contain leading or trailing spaces
		And account numbers with extra whitespace should be flagged
		And flagged accounts should be logged for manual correction
Examples:
| file_name                                | sheet_name |
| bank_export_invalid_account_whitespace.csv   | N/A        |
| bank_export_invalid_account_whitespace.xlsx  | Sheet1     |
@whitespace_handling @transaction_id @data_integrity
Scenario Outline: Detect whitespace issues in transaction IDs
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" column in the "<sheet_name>" sheet
	Then transaction IDs should not contain leading or trailing spaces
		And transaction IDs with extra spaces should be flagged
		And flagged transactions should be reviewed manually
Examples:
| file_name                                  | sheet_name |
| bank_export_invalid_transaction_whitespace.csv  | N/A        |
| bank_export_invalid_transaction_whitespace.xlsx | Sheet1     |
@whitespace_handling @currency_codes @data_consistency
Scenario Outline: Ensure currency codes do not contain extra spaces
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then currency codes should not have leading or trailing spaces
		And currency codes with extra whitespace should be flagged
		And flagged transactions should be reviewed manually
Examples:
| file_name                                | sheet_name |
| bank_export_invalid_currency_whitespace.csv  | N/A        |
| bank_export_invalid_currency_whitespace.xlsx | Sheet1     |
@whitespace_handling @edge_case @large_files @performance
Scenario Outline: Validate whitespace handling in large datasets
	Given a bank export file "<file_name>"
	When I check for whitespace issues in a file with more than 100,000 rows
	Then all occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And a detailed report should be generated with flagged records
Examples:
| file_name                                | sheet_name |
| bank_export_large_file_whitespace.csv | N/A        |
| bank_export_large_file_whitespace.xlsx | Sheet1     |
@whitespace_handling @high_risk @fraud_detection
Scenario Outline: Detect suspicious usage of whitespace in high-risk transactions
	Given a bank export file "<file_name>"
	When I check for whitespace issues in the "<column_name>" column in the "<sheet_name>" sheet
	Then transactions with excessive whitespace should be flagged
		And suspicious cases should trigger an alert for fraud analysis
		And flagged transactions should be escalated for further investigation
Examples:
| file_name                                | sheet_name | column_name  |
| bank_export_high_risk_whitespace.csv | N/A        | Description  |
| bank_export_high_risk_whitespace.xlsx | Sheet1     | Description  |
