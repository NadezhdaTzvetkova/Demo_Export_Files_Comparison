Feature: Detect Fraudulent Transactions in Export Files
@fraudulent_transactions @data_integrity @fraud_detection
Scenario Outline: Identify fraudulent transactions based on high-risk indicators
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" column in the "<sheet_name>" sheet
	Then transactions flagged with high-risk indicators should be identified
		And an alert should be generated for compliance review
		And flagged transactions should be escalated for investigation
Examples:
| file_name                                 | sheet_name |
| bank_export_fraudulent_transactions_test.csv | N/A        |
| bank_export_fraudulent_transactions_test.xlsx | Sheet1     |
@fraudulent_transactions @edge_case @amount_mismatch
Scenario Outline: Detect transactions with unusual amount variations
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Amount" columns in the "<sheet_name>" sheet
	Then transactions with inconsistent amounts should be flagged
		And transactions exceeding predefined thresholds should trigger an alert
		And flagged transactions should be reviewed manually for fraud risk
Examples:
| file_name                                          | sheet_name |
| bank_export_fraudulent_transactions_amount_mismatch.csv | N/A        |
| bank_export_fraudulent_transactions_amount_mismatch.xlsx | Sheet1     |
@fraudulent_transactions @data_quality @location_mismatch
Scenario Outline: Identify transactions with mismatched locations
	Given a bank export file "<file_name>"
	When I check the "Transaction ID" and "Location" columns in the "<sheet_name>" sheet
	Then transactions with conflicting locations within a short time frame should be flagged
		And flagged transactions should be reviewed for potential fraud patterns
		And system-generated recommendations should be provided for further investigation
Examples:
| file_name                                             | sheet_name |
| bank_export_fraudulent_transactions_location_mismatch.csv | N/A        |
| bank_export_fraudulent_transactions_location_mismatch.xlsx | Sheet1     |
@fraudulent_transactions @edge_case @large_files @performance
Scenario Outline: Validate fraudulent transaction detection in large datasets
	Given a bank export file "<file_name>"
	When I check for fraudulent transactions in a file with more than 100,000 rows
	Then all fraudulent occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And flagged fraud cases should be logged for auditing
Examples:
| file_name                                          | sheet_name |
| bank_export_large_file_fraudulent_transactions.csv | N/A        |
| bank_export_large_file_fraudulent_transactions.xlsx | Sheet1     |
@fraudulent_transactions @high_risk @fraud_patterns
Scenario Outline: Detect transactions linked to known fraud patterns
	Given a bank export file "<file_name>"
	When I check for high-risk transactions in the "<sheet_name>" sheet
	Then transactions matching known fraud patterns should be flagged
		And flagged cases should trigger an alert for regulatory compliance review
		And an escalation report should be generated for further investigation
Examples:
| file_name                                                | sheet_name |
| bank_export_high_risk_fraudulent_transactions.csv       | N/A        |
| bank_export_high_risk_fraudulent_transactions.xlsx      | Sheet1     |
