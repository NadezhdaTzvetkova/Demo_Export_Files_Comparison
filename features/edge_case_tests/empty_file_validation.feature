Feature: Handle Edge Cases in Export Files
@edge_cases @empty_files @validation
Scenario Outline: Validate handling of empty export files
	Given a bank export file "<file_name>"
	When I attempt to process the file
	Then the system should detect it as empty
		And an appropriate error message should be returned
		And the file should be excluded from processing
Examples:
| file_name                          |
| bank_export_empty_file.csv         |
| bank_export_empty_file.xlsx        |
@edge_cases @special_characters @data_quality
Scenario Outline: Detect and handle special characters in transaction data
	Given a bank export file "<file_name>"
	When I check for special characters in the "<column_name>" column
	Then transactions containing special characters should be flagged
		And flagged transactions should be reviewed for correction
		And a sanitized version of the data should be generated
Examples:
| file_name                          | column_name      |
| bank_export_special_chars.csv      | Description      |
| bank_export_special_chars.xlsx     | Account Name     |
@edge_cases @date_format @validation
Scenario Outline: Validate transactions with extreme date values
	Given a bank export file "<file_name>"
	When I check the "Date" column in the "<sheet_name>" sheet
	Then transactions with dates in the far future or past should be flagged
		And flagged transactions should trigger an alert for review
		And suggested corrections should be provided
Examples:
| file_name                          | sheet_name |
| bank_export_extreme_dates.csv      | N/A        |
| bank_export_extreme_dates.xlsx     | Sheet1     |
@edge_cases @large_files @performance
Scenario Outline: Test system performance with extremely large export files
	Given a bank export file "<file_name>"
	When I attempt to process the file
	Then the system should successfully process large data sets
		And response times should be logged for benchmarking
		And system memory consumption should remain within acceptable limits
Examples:
| file_name                          |
| bank_export_large_dataset.csv      |
| bank_export_large_dataset.xlsx     |
@edge_cases @inconsistent_delimiters @data_format
Scenario Outline: Detect and handle inconsistent delimiters in CSV files
	Given a bank export file "<file_name>"
	When I check the delimiter format
	Then the system should detect inconsistent delimiters
		And standardize the delimiter across the file
		And report any non-standard formatting
Examples:
| file_name                          |
| bank_export_inconsistent_delimiter.csv |
@edge_cases @corrupt_files @validation
Scenario Outline: Handle corrupted or unreadable export files
	Given a bank export file "<file_name>"
	When I attempt to open the file
	Then an error should be raised indicating the file is corrupted
		And the file should be excluded from processing
		And an alert should be generated for manual review
Examples:
| file_name                          |
| bank_export_corrupt_file.csv       |
| bank_export_corrupt_file.xlsx      |
@edge_cases @whitespace_issues @data_sanitization
Scenario Outline: Validate handling of excessive whitespace in data fields
	Given a bank export file "<file_name>"
	When I check for whitespace issues in the "<column_name>" column
	Then leading and trailing spaces should be removed
		And multiple consecutive spaces should be collapsed
		And sanitized data should be provided as output
Examples:
| file_name                          | column_name      |
| bank_export_whitespace.csv         | Account Name     |
| bank_export_whitespace.xlsx        | Description      |
