Feature: Detect Duplicate Account Numbers in Export Files
@duplicate_accounts @data_integrity @account_validation
Scenario Outline: Identify duplicate account numbers in transaction records
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then duplicate account numbers should be flagged
		And a report should be generated listing duplicate occurrences
		And accounts with high-frequency duplication should be escalated for review
Examples:
| file_name                                | sheet_name |
| bank_export_duplicate_accounts_test.csv | N/A        |
| bank_export_duplicate_accounts_test.xlsx | Sheet1     |
@duplicate_accounts @edge_case @linked_transactions
Scenario Outline: Detect transactions with duplicate accounts but different names
	Given a bank export file "<file_name>"
	When I check transactions in the "<sheet_name>" sheet
	Then account numbers with different associated names should be flagged
		And a fraud alert should be raised for investigation
		And an audit trail should be created to track duplicate accounts
Examples:
| file_name                                      | sheet_name |
| bank_export_duplicate_accounts_diff_names.csv | N/A        |
| bank_export_duplicate_accounts_diff_names.xlsx | Sheet1     |
@duplicate_accounts @data_quality @missing_values
Scenario Outline: Identify duplicate accounts with missing mandatory fields
	Given a bank export file "<file_name>"
	When I check the "Account Number" and "Account Holder Name" columns in the "<sheet_name>" sheet
	Then duplicate account numbers with missing values should be flagged
		And incomplete records should be marked for manual review
		And suggestions should be provided for data completion
Examples:
| file_name                                      | sheet_name |
| bank_export_duplicate_accounts_missing_fields.csv | N/A        |
| bank_export_duplicate_accounts_missing_fields.xlsx | Sheet1     |
@duplicate_accounts @edge_case @large_files @performance
Scenario Outline: Validate duplicate account detection in large datasets
	Given a bank export file "<file_name>"
	When I check for duplicate accounts in a file with more than 100,000 rows
	Then all duplicate occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And flagged duplicates should be logged for auditing
Examples:
| file_name                                       | sheet_name |
| bank_export_large_file_duplicate_accounts.csv | N/A        |
| bank_export_large_file_duplicate_accounts.xlsx | Sheet1     |
@duplicate_accounts @high_risk @fraud_detection
Scenario Outline: Detect duplicate accounts linked to suspicious transactions
	Given a bank export file "<file_name>"
	When I check for duplicate accounts in high-risk transactions in the "<sheet_name>" sheet
	Then duplicate accounts linked to fraudulent transactions should be flagged
		And flagged cases should trigger a compliance alert
		And an escalation report should be generated for further review
Examples:
| file_name                                           | sheet_name |
| bank_export_high_risk_duplicate_accounts.csv       | N/A        |
| bank_export_high_risk_duplicate_accounts.xlsx      | Sheet1     |
