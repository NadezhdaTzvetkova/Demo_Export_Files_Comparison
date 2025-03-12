Feature: Validate Currency Consistency

Scenario Outline: Ensure all currency values follow ISO 4217 format
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then all currency values should be valid ISO 4217 codes
		And currency codes should be consistent with account country
		And transactions with invalid currency codes should be flagged
		And currency values should not contain special characters or spaces
Examples:
| file_name                                      | sheet_name |
| bank_export_baseline_test.csv                 | N/A        |
| bank_export_baseline_test.xlsx                | Sheet1     |
Scenario Outline: Detect currency mismatches between accounts and transactions
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then each transaction currency should match the associated account currency
		And currency mismatches should be logged for review
		And the system should suggest potential corrections for mismatches
Examples:
| file_name                                     | sheet_name |
| bank_export_currency_mismatch_test.csv       | N/A        |
| bank_export_currency_mismatch_test.xlsx      | Sheet1     |
Scenario Outline: Ensure currency conversion rates are correctly applied
	Given a bank export file "<file_name>"
	When I check the "Exchange Rate" column in the "<sheet_name>" sheet
	Then exchange rates should be correctly applied for non-local transactions
		And transactions with incorrect exchange rates should be flagged
		And exchange rates should match official central bank rates within tolerance limits
Examples:
| file_name                                 | sheet_name |
| bank_export_foreign_transactions_test.csv | N/A        |
| bank_export_foreign_transactions_test.xlsx| Sheet1     |
Scenario Outline: Detect currency inconsistencies in multi-currency transactions
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then multi-currency transactions should have valid conversion rates
		And cross-currency transactions should be balanced correctly
		And any currency fluctuation anomalies should be reported
Examples:
| file_name                                 | sheet_name |
| bank_export_multi_currency_test.csv      | N/A        |
| bank_export_multi_currency_test.xlsx     | Sheet1     |
Scenario Outline: Ensure no missing or blank currency values
	Given a bank export file "<file_name>"
	When I check the "Currency" column in the "<sheet_name>" sheet
	Then there should be no missing or blank currency values
		And missing currency values should be flagged
		And the system should auto-fill missing values based on transaction context when possible
Examples:
| file_name                                | sheet_name |
| bank_export_missing_currency_test.csv   | N/A        |
| bank_export_missing_currency_test.xlsx  | Sheet1     |
