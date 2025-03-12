Feature: Detect Duplicate Customer Records in Export Files
@duplicate_customers @data_integrity @customer_validation
Scenario Outline: Identify duplicate customer records in the database
	Given a bank export file "<file_name>"
	When I check the "Customer ID" column in the "<sheet_name>" sheet
	Then duplicate customer records should be flagged
		And a report should be generated listing duplicate occurrences
		And duplicate customers should be marked for manual review
Examples:
| file_name                               | sheet_name |
| bank_export_duplicate_customers_test.csv | N/A        |
| bank_export_duplicate_customers_test.xlsx | Sheet1     |
@duplicate_customers @edge_case @name_variations
Scenario Outline: Detect duplicate customers with name variations
	Given a bank export file "<file_name>"
	When I check the "Customer Name" and "Customer ID" columns in the "<sheet_name>" sheet
	Then customer records with matching IDs but different names should be flagged
		And an audit trail should be created for potential fraud investigation
		And a suggestion should be generated for possible name standardization
Examples:
| file_name                                      | sheet_name |
| bank_export_duplicate_customers_name_variations.csv | N/A        |
| bank_export_duplicate_customers_name_variations.xlsx | Sheet1     |
@duplicate_customers @data_quality @missing_values
Scenario Outline: Identify duplicate customers with missing mandatory fields
	Given a bank export file "<file_name>"
	When I check the "Customer ID" and "Customer Name" columns in the "<sheet_name>" sheet
	Then duplicate customers with missing values should be flagged
		And incomplete records should be marked for manual review
		And an automated recommendation should be provided to correct missing values
Examples:
| file_name                                      | sheet_name |
| bank_export_duplicate_customers_missing_fields.csv | N/A        |
| bank_export_duplicate_customers_missing_fields.xlsx | Sheet1     |
@duplicate_customers @edge_case @large_files @performance
Scenario Outline: Validate duplicate customer detection in large datasets
	Given a bank export file "<file_name>"
	When I check for duplicate customers in a file with more than 100,000 rows
	Then all duplicate occurrences should be detected efficiently
		And system performance should be benchmarked for optimization
		And flagged duplicates should be logged for auditing
Examples:
| file_name                                       | sheet_name |
| bank_export_large_file_duplicate_customers.csv | N/A        |
| bank_export_large_file_duplicate_customers.xlsx | Sheet1     |
@duplicate_customers @high_risk @fraud_detection
Scenario Outline: Detect duplicate customers linked to suspicious transactions
	Given a bank export file "<file_name>"
	When I check for duplicate customers in high-risk transactions in the "<sheet_name>" sheet
	Then duplicate customer records involved in fraudulent transactions should be flagged
		And flagged cases should trigger an alert for compliance review
		And an escalation report should be generated for further investigation
Examples:
| file_name                                           | sheet_name |
| bank_export_high_risk_duplicate_customers.csv       | N/A        |
| bank_export_high_risk_duplicate_customers.xlsx      | Sheet1     |
