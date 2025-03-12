Feature: Validate Invalid Account Numbers
@account_validation @format_check
Scenario Outline: Ensure all account numbers follow the correct format
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then all account numbers should match the expected pattern "<pattern>"
		And invalidly formatted account numbers should be flagged
		And a correction suggestion should be provided
		And an alert should be sent for accounts not matching regulatory formats
Examples:
| file_name                              | sheet_name | pattern        |
| bank_export_baseline_test.csv         | N/A        | ^\d{10,12}$    |
| bank_export_baseline_test.xlsx        | Sheet1     | ^\d{10,12}$    |
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
@account_validation @duplicate_accounts @high_risk
Scenario Outline: Detect duplicate account numbers
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in the "<sheet_name>" sheet
	Then duplicate account numbers should be flagged
		And a list of duplicate occurrences should be generated
		And accounts with multiple transactions under different names should be flagged for fraud review
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
@account_validation @edge_case @large_files @performance
Scenario Outline: Validate account numbers in large files
	Given a bank export file "<file_name>"
	When I check the "Account Number" column in a file with more than 100,000 rows
	Then all account numbers should maintain format consistency
		And inconsistencies should be flagged for bulk correction
		And performance benchmarks should be recorded
		And large volume discrepancies should be analyzed for system optimization
Examples:
| file_name                               | sheet_name |
| bank_export_large_file_accounts_test.csv | N/A        |
| bank_export_large_file_accounts_test.xlsx | Sheet1     |
@account_validation @edge_case @blacklisted_accounts
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
