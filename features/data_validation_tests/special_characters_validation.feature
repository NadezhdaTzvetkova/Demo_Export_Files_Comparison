Feature: Validate Special Characters in Export Files
@special_characters @data_quality @field_validation
Scenario Outline: Ensure fields do not contain invalid special characters
	Given a bank export file "<file_name>"
	When I check for special characters in the "<column_name>" column in the "<sheet_name>" sheet
	Then special characters should not be present unless explicitly allowed
		And values containing special characters should be flagged
		And a correction suggestion should be provided
Examples:
| file_name                              | sheet_name | column_name     |
| bank_export_baseline_test.csv         | N/A        | Description     |
| bank_export_baseline_test.xlsx        | Sheet1     | Description     |
@special_characters @account_numbers @edge_case
Scenario Outline: Detect special characters in account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then account numbers should contain only numeric values
		And account numbers containing special characters should be flagged
		And flagged accounts should be logged for manual correction
Examples:
| file_name                                | sheet_name |
| bank_export_invalid_account_chars.csv   | N/A        |
| bank_export_invalid_account_chars.xlsx  | Sheet1     |
@special_characters @transaction_id @data_integrity
Scenario Outline: Detect special characters in transaction IDs
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" column in the "<sheet_name>" sheet
	Then transaction IDs should only contain alphanumeric characters
		And transaction IDs with special characters should be flagged
		And flagged transactions should be reviewed manually
Examples:
| file_name                                  | sheet_name |
| bank_export_invalid_transaction_ids.csv  | N/A        |
| bank_export_invalid_transaction_ids.xlsx | Sheet1     |
@special_characters @currency_codes @data_consistency
Scenario Outline: Ensure currency codes do not contain special characters
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then currency codes should match the expected format "^[A-Z]{3}$"
		And currency codes with special characters should be flagged
		And flagged transactions should be reviewed manually
Examples:
| file_name                                | sheet_name |
| bank_export_invalid_currency_chars.csv  | N/A        |
| bank_export_invalid_currency_chars.xlsx | Sheet1     |
@special_characters @edge_case @large_files @performance
Scenario Outline: Validate special character occurrences in large datasets
	Given a bank export file "<file_name>"
	When I check for special characters in a file with more than 100,000 rows
	Then all occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And a detailed report should be generated with flagged records
Examples:
| file_name                                | sheet_name |
| bank_export_large_file_special_chars.csv | N/A        |
| bank_export_large_file_special_chars.xlsx | Sheet1     |
@special_characters @high_risk @fraud_detection
Scenario Outline: Detect suspicious usage of special characters in high-risk transactions
	Given a bank export file "<file_name>"
	When I check for special characters in the "<column_name>" column in the "<sheet_name>" sheet
	Then transactions with excessive special characters should be flagged
		And suspicious cases should trigger an alert for fraud analysis
		And flagged transactions should be escalated for further investigation
Examples:
| file_name                                | sheet_name | column_name  |
| bank_export_high_risk_special_chars.csv | N/A        | Description  |
| bank_export_high_risk_special_chars.xlsx | Sheet1     | Description  |
