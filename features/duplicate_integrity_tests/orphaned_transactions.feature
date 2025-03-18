Feature: Detect Orphaned Transactions in Export Files
@orphaned_transactions @data_integrity @transaction_validation
Scenario Outline: Identify transactions without a linked account
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Account Number" columns in the "<sheet_name>" sheet
	Then transactions with missing or unlinked accounts should be flagged
		And an alert should be generated for data consistency review
		And flagged transactions should be escalated for manual verification
Examples:
| file_name                                 | sheet_name |
| bank_export_orphaned_transactions_test.csv | N/A        |
| bank_export_orphaned_transactions_test.xlsx | Sheet1     |
@orphaned_transactions @edge_case @mislinked_accounts
Scenario Outline: Detect transactions linked to non-existent accounts
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Account Number" columns in the "<sheet_name>" sheet
	Then transactions linked to accounts that do not exist in the database should be flagged
		And a reconciliation report should be generated
		And flagged cases should be escalated for correction
Examples:
| file_name                                      | sheet_name |
| bank_export_orphaned_transactions_mislinked.csv | N/A        |
| bank_export_orphaned_transactions_mislinked.xlsx | Sheet1     |
@orphaned_transactions @data_quality @missing_account_names
Scenario Outline: Identify transactions with missing account holder names
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Account Holder Name" columns in the "<sheet_name>" sheet
	Then transactions with missing account holder names should be flagged
		And incomplete records should be marked for manual review
		And an automated recommendation should be provided to correct missing values
Examples:
| file_name                                         | sheet_name |
| bank_export_orphaned_transactions_missing_names.csv | N/A        |
| bank_export_orphaned_transactions_missing_names.xlsx | Sheet1     |
@orphaned_transactions @edge_case @large_files @performance
Scenario Outline: Validate orphaned transaction detection in large datasets
	Given a bank export file "<file_name>"
	When I check for orphaned transactions in a file with more than 100,000 rows
	Then all orphaned occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And flagged orphaned transactions should be logged for auditing
Examples:
| file_name                                        | sheet_name |
| bank_export_large_file_orphaned_transactions.csv | N/A        |
| bank_export_large_file_orphaned_transactions.xlsx | Sheet1     |
@orphaned_transactions @high_risk @fraud_detection
Scenario Outline: Detect orphaned transactions linked to suspicious activities
	Given a bank export file "<file_name>"
	When I check for orphaned transactions in high-risk transactions in the "<sheet_name>" sheet
	Then orphaned transactions linked to fraudulent activities should be flagged
		And flagged cases should trigger an alert for compliance review
		And an escalation report should be generated for further investigation
Examples:
| file_name                                                | sheet_name |
| bank_export_high_risk_orphaned_transactions.csv       | N/A        |
| bank_export_high_risk_orphaned_transactions.xlsx      | Sheet1     |
