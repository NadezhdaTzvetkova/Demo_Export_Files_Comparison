Feature: Detect Duplicate Transactions in Export Files
@duplicate_transactions @data_integrity @transaction_validation
Scenario Outline: Identify duplicate transaction records in the database
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" column in the "<sheet_name>" sheet
	Then duplicate transaction records should be flagged
		And a report should be generated listing duplicate occurrences
		And duplicate transactions should be marked for manual review
Examples:
| file_name                                 | sheet_name |
| bank_export_duplicate_transactions_test.csv | N/A        |
| bank_export_duplicate_transactions_test.xlsx | Sheet1     |
@duplicate_transactions @edge_case @amount_mismatch
Scenario Outline: Detect duplicate transactions with different amounts
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Amount" columns in the "<sheet_name>" sheet
	Then transactions with matching IDs but different amounts should be flagged
		And a potential data entry error should be reported
		And flagged transactions should be escalated for further validation
Examples:
| file_name                                           | sheet_name |
| bank_export_duplicate_transactions_amount_mismatch.csv | N/A        |
| bank_export_duplicate_transactions_amount_mismatch.xlsx | Sheet1     |
@duplicate_transactions @data_quality @timestamp_variance
Scenario Outline: Identify duplicate transactions with timestamp variations
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Timestamp" columns in the "<sheet_name>" sheet
	Then transactions with identical IDs but differing timestamps should be flagged
		And flagged transactions should be reviewed for potential system processing errors
Examples:
| file_name                                             | sheet_name |
| bank_export_duplicate_transactions_timestamp_variance.csv | N/A        |
| bank_export_duplicate_transactions_timestamp_variance.xlsx | Sheet1     |
@duplicate_transactions @edge_case @large_files @performance
Scenario Outline: Validate duplicate transaction detection in large datasets
	Given a bank export file "<file_name>"
	When I check for duplicate transactions in a file with more than 100,000 rows
	Then all duplicate occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And flagged duplicates should be logged for auditing
Examples:
| file_name                                         | sheet_name |
| bank_export_large_file_duplicate_transactions.csv | N/A        |
| bank_export_large_file_duplicate_transactions.xlsx | Sheet1     |
@duplicate_transactions @high_risk @fraud_detection
Scenario Outline: Detect duplicate transactions linked to suspicious activities
	Given a bank export file "<file_name>"
	When I check for duplicate transactions in high-risk transactions in the "<sheet_name>" sheet
	Then duplicate transactions linked to fraudulent activities should be flagged
		And flagged cases should trigger an alert for compliance review
		And an escalation report should be generated for further investigation
Examples:
| file_name                                               | sheet_name |
| bank_export_high_risk_duplicate_transactions.csv       | N/A        |
| bank_export_high_risk_duplicate_transactions.xlsx      | Sheet1     |
