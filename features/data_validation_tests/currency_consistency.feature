Feature: Validate Currency Consistency and Negative Values in Exported Bank Files
@currency_consistency @data_quality @transaction_validation
Scenario Outline: Ensure currency codes are correctly recorded
	Given a bank export file "<file_name>"
	When I check for currency codes in the "<sheet_name>" sheet
	Then all transactions should have a valid ISO 4217 currency code
		And currency codes should match the account’s assigned currency
		And mismatches should be flagged with "<severity>"
Examples:
| file_name                               | sheet_name | severity  |
| bank_export_currency_test.csv           | N/A        | High      |
| bank_export_currency_test.xlsx          | Sheet1     | Medium    |
@currency_consistency @negative_values @debit_credit_validation
Scenario Outline: Ensure negative values are correctly recorded
	Given a bank export file "<file_name>"
	When I check for negative values in the "<sheet_name>" sheet
	Then negative values should only be present in debit transactions
		And credit transactions should not have negative values
		And incorrect negative values should be flagged for review
		And a correction suggestion should be provided
Examples:
| file_name                              | sheet_name |
| bank_export_baseline_test.csv          | N/A        |
| bank_export_baseline_test.xlsx         | Sheet1     |
@currency_consistency @zero_amounts @edge_case
Scenario Outline: Detect zero and negative transaction amounts
	Given a bank export file "<file_name>"
	When I check for negative and zero values in the "<sheet_name>" sheet
	Then negative amounts should only exist for debit transactions
		And zero amounts should be flagged as potential errors
		And transactions with zero values should be logged for further review
Examples:
| file_name                              | sheet_name |
| bank_export_negative_values_test.csv   | N/A        |
| bank_export_negative_values_test.xlsx  | Sheet1     |
@currency_consistency @exchange_rate_validation @data_consistency
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
@currency_consistency @multi_currency @exchange_rate_accuracy
Scenario Outline: Ensure correct exchange rate usage for multi-currency transactions
	Given a bank export file "<file_name>" with multi-currency transactions
	When the system calculates equivalent transaction amounts
	Then exchange rates should match the reference data "<exchange_rate_file>"
		And mismatches beyond "<tolerance>%" should be flagged as "<severity>"
Examples:
| file_name                        | exchange_rate_file            | tolerance | severity  |
| transactions_forex_rates.csv     | official_exchange_rates.csv   | 0.5       | High      |
| transactions_forex_incorrect.xlsx| outdated_rates.xlsx           | 1.0       | Medium    |
@currency_consistency @large_files @performance
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
@currency_consistency @high_risk @fraud_detection
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
@currency_consistency @performance_testing
Scenario Outline: Assess system performance for currency consistency validation
	Given a system processing "<file_count>" bank export files per hour
	When transactions have varying currencies and exchange rates
	Then processing should complete within "<expected_time>" seconds
		And system resource usage should not exceed "<resource_limit>%"
Examples:
| file_count | expected_time | resource_limit |
| 1000       | 600           | 75            |
| 5000       | 1200          | 85            |
@currency_consistency @schema_validation
Scenario Outline: Validate system behavior for schema mismatches due to currency inconsistencies
	Given an export file "<file_name>" with schema "<schema_type>"
	When I check the schema validation rules
	Then currency format mismatches should be flagged as "<error_severity>"
		And system logs should capture all schema-related discrepancies
		And if possible, correction mappings should be suggested to match "<expected_format>"
Examples:
| file_name                    | schema_type       | expected_format    | error_severity |
| transactions_legacy.csv       | Legacy Format    | Standard V1.2      | High           |
| transactions_modified.xlsx    | Custom Schema    | Standard V1.3      | Medium         |
| transactions_test.csv         | Test Environment | Test Format V2.0   | Low            |
