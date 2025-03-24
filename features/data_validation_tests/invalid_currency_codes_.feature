Feature: Validate Invalid Currency Codes in Bank Export Files
@currency_validation @format_check @data_integrity

Scenario Outline: Ensure all currency codes follow ISO 4217 standard
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then all currency codes should match the expected pattern "<pattern>"
	And invalid currency codes should be flagged
	And a correction suggestion should be provided
	And transactions with invalid currency codes should be marked for review


Examples:
| file_name                              | sheet_name | pattern     |
| bank_export_baseline_test.csv         | N/A        | ^[A-Z]{3}$  |
| bank_export_baseline_test.xlsx        | Sheet1     | ^[A-Z]{3}$  |
@currency_validation @aml_compliance @sanctions_check

Scenario Outline: Detect transactions involving sanctioned or restricted currency codes
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then currency codes listed under sanctioned countries should be flagged
	And flagged transactions should be logged for compliance review
	And an alert should be sent to regulatory teams


Examples:
| file_name                                    | sheet_name |
| bank_export_sanctioned_currencies_test.csv  | N/A        |
| bank_export_sanctioned_currencies_test.xlsx | Sheet1     |
@currency_validation @invalid_characters @edge_case

Scenario Outline: Detect currency codes with special characters, numbers, or unexpected symbols
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then currency codes containing non-alphabetic characters should be flagged
	And an error report should be generated with affected transactions
	And transactions linked to invalid currency codes should be flagged for further review


Examples:
| file_name                                | sheet_name |
| bank_export_invalid_currency_chars.csv  | N/A        |
| bank_export_invalid_currency_chars.xlsx | Sheet1     |
@currency_validation @non_standard_codes @deprecated_currencies

Scenario Outline: Detect non-standard, deprecated, or obsolete currency codes
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then deprecated or non-standard currency codes should be flagged
	And a list of deprecated currency codes should be generated
	And transactions involving non-standard currencies should be reviewed manually


Examples:
| file_name                               | sheet_name |
| bank_export_deprecated_currency_test.csv | N/A        |
| bank_export_deprecated_currency_test.xlsx | Sheet1     |
@currency_validation @missing_values @data_quality

Scenario Outline: Ensure no missing or blank currency codes
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then no currency field should be empty or null
	And missing currency codes should be flagged
	And an auto-fill suggestion should be provided if possible
	And transactions missing a currency code should be categorized separately for investigation


Examples:
| file_name                              | sheet_name |
| bank_export_missing_currency_test.csv | N/A        |
| bank_export_missing_currency_test.xlsx | Sheet1     |
@currency_validation @large_files @performance_testing

Scenario Outline: Validate currency codes in large-scale financial transactions
	Given a bank export file "<file_name>"
	When I check the "Currency" column in a file with "<row_count>" rows
	Then all currency codes should maintain format consistency
	And inconsistencies should be flagged for bulk correction
	And system performance should be benchmarked for optimization


Examples:
| file_name                               | row_count |
| bank_export_large_file_currency_test.csv | 100000   |
| bank_export_large_file_currency_test.xlsx | 500000   |
@currency_validation @edge_case @restricted_currencies

Scenario Outline: Detect restricted or high-risk currency codes
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then currency codes associated with sanctioned or restricted countries should be flagged
	And flagged transactions should be logged for compliance review
	And an alert should be sent to regulatory teams


Examples:
| file_name                                    | sheet_name |
| bank_export_restricted_currency_test.csv   | N/A        |
| bank_export_restricted_currency_test.xlsx  | Sheet1     |
@currency_validation @crypto_currency @digital_assets

Scenario Outline: Identify crypto-based or unauthorized digital currency transactions
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then cryptocurrency symbols (e.g., BTC, ETH) should be flagged if not permitted
	And unauthorized transactions should be escalated for fraud review
	And an alert should be generated for regulatory compliance teams


Examples:
| file_name                               |
| bank_export_crypto_currency_test.csv   |
| bank_export_crypto_currency_test.xlsx  |
@currency_validation @exchange_rate_consistency @cross_currency_transactions

Scenario Outline: Ensure currency codes align with correct exchange rates
	Given a bank export file "<file_name>"
	When I check the "Currency" and "Exchange Rate" columns in the "<sheet_name>" sheet
	Then currency codes should be valid per ISO 4217 standards
	And exchange rates should match the official daily conversion rates
	And discrepancies should be flagged for review


Examples:
| file_name                                    | sheet_name |
| bank_export_cross_currency_transactions.csv | N/A        |
| bank_export_cross_currency_transactions.xlsx | Sheet1     |
