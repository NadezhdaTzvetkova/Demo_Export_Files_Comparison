Feature: Validate Invalid Account Numbers in Bank Export Files
@account_validation @format_check @data_integrity
Scenario Outline: Ensure all account numbers follow the correct format
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then all account numbers should match the expected pattern "<pattern>"
		And invalidly formatted account numbers should be flagged
		And a correction suggestion should be provided
		And an alert should be sent for accounts not matching regulatory formats
Examples:
| file_name                              | sheet_name | pattern         |
| bank_export_baseline_test.csv         | N/A        | ^\d{10,12}$     |
| bank_export_baseline_test.xlsx        | Sheet1     | ^\d{10,12}$     |
@account_validation @iban_check @regulatory_compliance
Scenario Outline: Validate IBAN compliance for international transactions
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then all IBAN numbers should be valid according to country-specific rules
		And invalid IBANs should be flagged for correction
		And a report should list all incorrectly formatted IBANs
Examples:
| file_name                              | sheet_name |
| bank_export_iban_validation_test.csv  | N/A        |
| bank_export_iban_validation_test.xlsx | Sheet1     |
@account_validation @invalid_characters @edge_case
Scenario Outline: Detect account numbers with special characters or alphabets
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then account numbers containing non-numeric characters should be flagged
		And an error report should be generated with affected accounts
		And transactions linked to invalid accounts should be flagged for further review
Examples:
| file_name                                | sheet_name |
| bank_export_invalid_characters_test.csv | N/A        |
| bank_export_invalid_characters_test.xlsx | Sheet1     |
@account_validation @duplicate_accounts @fraud_detection
Scenario Outline: Detect duplicate account numbers with mismatched account holder names
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then duplicate account numbers should be flagged
		And mismatched account holders for the same account should trigger a fraud alert
		And transactions under duplicated accounts should be reviewed
Examples:
| file_name                               | sheet_name |
| bank_export_duplicate_accounts_test.csv | N/A        |
| bank_export_duplicate_accounts_test.xlsx | Sheet1     |
@account_validation @missing_values @data_quality
Scenario Outline: Ensure no missing or blank account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then no account field should be empty or null
		And missing account numbers should be flagged
		And an auto-fill suggestion should be provided if possible
		And transactions missing an account number should be categorized separately for investigation
Examples:
| file_name                              | sheet_name |
| bank_export_missing_accounts_test.csv | N/A        |
| bank_export_missing_accounts_test.xlsx | Sheet1     |
@account_validation @large_files @performance_testing
Scenario Outline: Validate account numbers in large datasets
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in a file with "<row_count>" rows
	Then all account numbers should maintain format consistency
		And inconsistencies should be flagged for bulk correction
		And system performance should be benchmarked for optimization
Examples:
| file_name                               | row_count |
| bank_export_large_file_accounts_test.csv | 100000   |
| bank_export_large_file_accounts_test.xlsx | 500000   |
@account_validation @blacklisted_accounts @high_risk_accounts
Scenario Outline: Detect blacklisted or restricted account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then accounts matching known blacklisted or restricted patterns should be flagged
		And flagged accounts should be logged for review
		And an alert should be sent to compliance teams
Examples:
| file_name                                    | sheet_name |
| bank_export_blacklisted_accounts_test.csv   | N/A        |
| bank_export_blacklisted_accounts_test.xlsx  | Sheet1     |
@account_validation @account_truncation @data_integrity
Scenario Outline: Identify truncated or improperly padded account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then account numbers shorter than "<min_length>" digits should be flagged
		And excessively padded account numbers should be normalized
		And truncation issues should be logged for correction
Examples:
| file_name                               | min_length |
| bank_export_truncated_accounts_test.csv | 10         |
| bank_export_truncated_accounts_test.xlsx | 12         |
@account_validation @bank_branch_codes @institutional_accounts
Scenario Outline: Validate bank-specific account structures with branch codes
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then account numbers should include valid branch and institution codes "<branch_format>"
		And invalid structures should be flagged for correction
		And system logs should highlight mismatched formats for review
Examples:
| file_name                               | branch_format |
| bank_export_branch_code_test.csv       | 4-digit prefix |
| bank_export_branch_code_test.xlsx      | 6-digit prefix |
@account_validation @account_closure_check @dormant_accounts
Scenario Outline: Detect transactions involving closed or dormant accounts
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then transactions linked to closed accounts should be flagged
		And an alert should be sent for manual review
		And affected transactions should be logged separately
Examples:
| file_name                                  |
| bank_export_closed_accounts_test.csv     |
| bank_export_closed_accounts_test.xlsx    |
@account_validation @error_handling @resilience_testing
Scenario Outline: Ensure system resilience against malformed account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then malformed account numbers should not crash the system
		And structured error handling should ensure continued processing
		And logs should capture all malformed entries for review
Examples:
| file_name                                |
| bank_export_malformed_accounts_test.csv |
| bank_export_malformed_accounts_test.xlsx |
