Feature: Handle Edge Cases in Export Files
@edge_cases @zero_value_transactions @data_integrity
Scenario Outline: Detect transactions with zero values
	Given a bank export file "<file_name>"
	When I analyze the "Amount" column in the "<sheet_name>" sheet
	Then transactions with an amount of zero should be flagged
		And flagged transactions should be logged for further review
		And recommendations for corrective action should be generated
		And the system should classify them based on "<transaction_type>"
Examples:
| file_name                              | sheet_name | transaction_type |
| bank_export_zero_value_transactions.csv  | N/A        | Standard        |
| bank_export_zero_value_transactions.xlsx | Sheet1     | High-Risk       |
@edge_cases @zero_value_transactions @fraud_detection
Scenario Outline: Identify zero-value transactions in high-risk categories
	Given a bank export file "<file_name>"
	When I check for zero-value transactions in the "<category>" category in the "<sheet_name>" sheet
	Then transactions with zero value in high-risk categories should be flagged as suspicious
		And flagged transactions should be escalated for compliance review
		And a fraud detection report should be generated
		And a risk assessment score should be assigned based on "<risk_level>"
Examples:
| file_name                                      | category                  | sheet_name | risk_level |
| bank_export_suspicious_zero_values.csv       | Wire Transfers            | N/A        | High       |
| bank_export_suspicious_zero_values.xlsx      | International Payments    | Sheet1     | Critical   |
| bank_export_suspicious_zero_values.xlsx      | Internal Transfers        | Sheet2     | Medium     |
@edge_cases @zero_value_transactions @data_quality @threshold
Scenario Outline: Validate zero-value transactions against historical patterns
	Given a bank export file "<file_name>"
	When I compare the "Amount" column with historical data
	Then transactions with zero value exceeding "<threshold>%" of total transactions should be flagged
		And corrective action should be suggested
		And an alert should be generated for data quality review
		And the threshold comparison should consider "<time_period>" historical data
Examples:
| file_name                              | threshold | time_period |
| bank_export_zero_value_trends.csv     | 5%        | Last 6 Months  |
| bank_export_zero_value_trends.xlsx    | 10%       | Last 12 Months |
@edge_cases @zero_value_transactions @performance
Scenario Outline: Test system performance when processing large datasets with zero-value transactions
	Given a bank export file "<file_name>"
	When I attempt to process a dataset containing more than "<row_count>" transactions with zero values
	Then the system should handle the data efficiently
		And processing time should be logged for benchmarking
		And flagged zero-value transactions should be included in the validation report
		And system resource utilization should remain within acceptable limits
Examples:
| file_name                                      | row_count |
| bank_export_large_zero_value_dataset.csv      | 100000    |
| bank_export_large_zero_value_dataset.xlsx     | 200000    |
@edge_cases @zero_value_transactions @business_logic
Scenario Outline: Ensure zero-value transactions comply with business rules
	Given a bank export file "<file_name>"
	When I validate the "Amount" column in "<sheet_name>"
	Then zero-value transactions should be checked against predefined business rules
		And exceptions should be made for "<exempt_category>"
		And a compliance report should be generated
Examples:
| file_name                                      | sheet_name | exempt_category |
| bank_export_zero_value_compliance.csv        | N/A        | Fee Waivers     |
| bank_export_zero_value_compliance.xlsx       | Sheet1     | Government Rebates |
