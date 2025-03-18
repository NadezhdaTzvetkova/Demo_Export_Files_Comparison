Feature: Validate Decimal Precision Consistency in Exported Bank Files
@decimal_precision @format_check
Scenario Outline: Ensure all monetary values follow correct decimal precision
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then all monetary values should have exactly "<expected_precision>" decimal places
		And values should not contain more than "<expected_precision>" decimal places
		And rounding inconsistencies should be flagged
Examples:
| file_name                           | sheet_name | expected_precision |
| bank_export_baseline_test.csv       | N/A        | 2                  |
| bank_export_baseline_test.xlsx      | Sheet1     | 2                  |
@decimal_precision @rounding_errors @edge_case
Scenario Outline: Detect incorrect decimal precision values
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then values with more than "<max_allowed_precision>" decimal places should be flagged
		And rounding errors should be logged with suggested corrections
Examples:
| file_name                                | sheet_name | max_allowed_precision |
| bank_export_decimal_precision_test.csv  | N/A        | 2                     |
| bank_export_decimal_precision_test.xlsx | Sheet1     | 2                     |
@decimal_precision @large_transactions @financial_compliance
Scenario Outline: Ensure large transactions maintain correct decimal precision
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then large transactions above "<threshold_amount>" should have correctly formatted decimal precision
		And any rounding discrepancies should be reported
		And scientific notation should not be used
Examples:
| file_name                                | sheet_name | threshold_amount |
| bank_export_large_transactions_test.csv  | N/A        | 1,000,000        |
| bank_export_large_transactions_test.xlsx | Sheet1     | 1,000,000        |
@decimal_precision @negative_values @data_integrity
Scenario Outline: Ensure decimal precision is maintained for negative transactions
	Given a bank export file "<file_name>"
	When I check the "Amount" column in the "<sheet_name>" sheet
	Then negative values should have consistent decimal precision
		And any discrepancies in negative amounts should be flagged
		And transactions marked as refunds should retain precision without rounding issues
Examples:
| file_name                             | sheet_name |
| bank_export_negative_values_test.csv  | N/A        |
| bank_export_negative_values_test.xlsx | Sheet1     |
@decimal_precision @currency_conversion @exchange_rate_validation
Scenario Outline: Validate decimal precision for foreign currency conversions
	Given a bank export file "<file_name>"
	When I check the "Amount" and "Exchange Rate" columns in the "<sheet_name>" sheet
	Then converted values should maintain accurate decimal precision as per "<currency_standard>"
		And rounding should be consistent with financial regulations
		And discrepancies should be logged for review
Examples:
| file_name                                 | sheet_name | currency_standard |
| bank_export_foreign_transactions_test.csv | N/A        | ISO 4217          |
| bank_export_foreign_transactions_test.xlsx| Sheet1     | ISO 4217          |
@decimal_precision @multi_currency @locale_check
Scenario Outline: Validate different decimal precision rules for multiple currencies
	Given a bank export file "<file_name>"
	When I check monetary values in "<currency_code>" transactions
	Then decimal precision should match the expected standard "<expected_precision>"
		And transactions should be converted correctly based on their regional standards
Examples:
| file_name                               | currency_code | expected_precision |
| bank_export_mixed_currency_test.csv    | USD           | 2                  |
| bank_export_mixed_currency_test.xlsx   | JPY           | 0                  |
| bank_export_mixed_currency_test.xlsx   | KWD           | 3                  |
@decimal_precision @high_volume_transactions @performance_testing
Scenario Outline: Assess system performance for decimal precision validation in high-volume transactions
	Given a system processing "<file_count>" bank export files per hour
	When decimal validation is performed on "<transaction_count>" transactions
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
Examples:
| file_count | transaction_count | expected_time | resource_limit |
| 1000       | 1,000,000         | 300           | 75            |
| 5000       | 5,000,000         | 600           | 85            |
@decimal_precision @regulatory_compliance @financial_reporting
Scenario Outline: Validate decimal precision in regulatory financial reports
	Given a bank export file "<file_name>"
	When I check decimal precision in "<report_type>"
	Then all monetary fields should adhere to "<regulatory_standard>"
		And discrepancies should be flagged for compliance review
Examples:
| file_name                               | report_type                  | regulatory_standard |
| bank_export_tax_filing_2023.csv        | Annual Tax Report            | IRS Financial Guide |
| bank_export_financial_statement.xlsx   | Q2 Earnings Report           | GAAP Accounting     |
@decimal_precision @corrupt_data_handling @edge_case
Scenario Outline: Detect corrupt or unreadable decimal values
	Given a bank export file "<file_name>"
	When I check the "Amount" column for anomalies
	Then corrupted or unreadable decimal values should be flagged as "<error_type>"
		And the file should be logged for manual review
Examples:
| file_name                               | error_type            |
| transactions_corrupt_decimals.csv      | Encoding Error        |
| transactions_unreadable_amounts.xlsx  | Parsing Failure       |
