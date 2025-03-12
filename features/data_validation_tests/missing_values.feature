Feature: Validate Missing Values in Export Files
@missing_values @data_quality @mandatory_fields
Scenario Outline: Ensure no mandatory fields are empty
	Given a bank export file "<file_name>"
	When I check for missing values in the "<sheet_name>" sheet
	Then no mandatory field should be empty or null
		And missing values should be flagged
		And the system should suggest potential corrections based on historical data
		And an error report should be generated listing affected rows
Examples:
| file_name                              | sheet_name |
| bank_export_baseline_test.csv         | N/A        |
| bank_export_baseline_test.xlsx        | Sheet1     |
@missing_values @transaction_data @edge_case
Scenario Outline: Detect missing values in key transaction fields
	Given a bank export file "<file_name>"
	When I check for missing values in the "<sheet_name>" sheet
	Then transaction fields such as "Transaction ID", "Date", "Amount", and "Account Number" should not be empty
		And missing values should be flagged for review
		And the system should validate if missing data can be inferred based on surrounding transactions
Examples:
| file_name                                | sheet_name |
| bank_export_missing_transaction_values.csv  | N/A        |
| bank_export_missing_transaction_values.xlsx | Sheet1     |
@missing_values @currency_codes @data_consistency
Scenario Outline: Detect missing currency codes and suggest corrections
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then missing currency codes should be flagged
		And the system should suggest the most probable currency based on account history
		And flagged transactions should be reviewed manually
Examples:
| file_name                               | sheet_name |
| bank_export_missing_currency_test.csv | N/A        |
| bank_export_missing_currency_test.xlsx | Sheet1     |
@missing_values @edge_case @large_files @performance
Scenario Outline: Validate missing values in large datasets
	Given a bank export file "<file_name>"
	When I check for missing values in a file with more than 100,000 rows
	Then all missing values should be detected efficiently
		And system performance should be benchmarked for optimization
		And a detailed report should be generated with missing value statistics
Examples:
| file_name                               | sheet_name |
| bank_export_large_file_missing_values.csv | N/A        |
| bank_export_large_file_missing_values.xlsx | Sheet1     |
@missing_values @high_risk @fraud_detection
Scenario Outline: Detect missing values in high-risk transactions
	Given a bank export file "<file_name>"
	When I check for missing values in the "<sheet_name>" sheet
	Then high-risk transactions missing key information should be flagged
		And missing values should trigger an alert for fraud analysis
		And flagged transactions should be escalated for further investigation
Examples:
| file_name                                  | sheet_name |
| bank_export_high_risk_missing_values.csv  | N/A        |
| bank_export_high_risk_missing_values.xlsx | Sheet1     |
