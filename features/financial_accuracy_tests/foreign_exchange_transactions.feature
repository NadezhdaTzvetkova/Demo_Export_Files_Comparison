@fx_transactions @currency_conversion
Scenario Outline: Validate exchange rates for foreign currency transactions
	Given a bank export file "<file_name>"
	When I check the "Currency", "Amount", and "Exchange Rate" columns in "<sheet_name>"
	Then the converted amount should match official exchange rates within "<tolerance>"
		And transactions exceeding "<alert_threshold>" should trigger a compliance review
Examples:
| file_name                               | sheet_name | tolerance | alert_threshold |
| bank_export_foreign_transactions.csv   | N/A        | 0.5%      | $50,000         |
| bank_export_high_risk_forex.xlsx      | Sheet1     | 0.3%      | $100,000        |
@financial_accuracy @forex_transactions @exchange_rates
Scenario Outline: Ensure correct application of exchange rates
	Given a bank export file "<file_name>"
	When I check the "Exchange Rate" column in the "<sheet_name>" sheet
	Then all exchange rates should be accurate and sourced from "<official_source>"
		And any discrepancies should be flagged for correction
Examples:
| file_name                              | sheet_name | official_source     |
| forex_transactions_baseline_test.csv  | N/A        | ECB Exchange Rates  |
| forex_transactions_baseline_test.xlsx | Sheet1     | Federal Reserve     |
@financial_accuracy @forex_conversion @data_integrity
Scenario Outline: Validate currency conversion calculations
	Given a bank export file "<file_name>"
	When I check "Original Amount" and "Converted Amount" in the "<sheet_name>" sheet
	Then all conversions should use the correct exchange rate from "<reference_date>"
		And rounding differences should not exceed "<rounding_tolerance>"
Examples:
| file_name                                  | sheet_name | reference_date | rounding_tolerance |
| forex_conversion_test.csv                 | N/A        | 2024-01-01     | 0.01 |
| forex_conversion_test.xlsx                | Sheet1     | 2024-01-01     | 0.01 |
@financial_accuracy @multi_currency_transactions @fraud_detection
Scenario Outline: Detect inconsistent multi-currency transactions
	Given a bank export file "<file_name>"
	When I check transactions involving multiple currencies in the "<sheet_name>" sheet
	Then transactions with conflicting or unsupported currency codes should be flagged
		And any unusual currency conversions should trigger an alert for fraud review
Examples:
| file_name                                  | sheet_name |
| forex_multi_currency_fraud_test.csv       | N/A        |
| forex_multi_currency_fraud_test.xlsx      | Sheet1     |
