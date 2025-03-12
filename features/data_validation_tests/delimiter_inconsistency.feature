Feature: Validate Delimiter Inconsistency
@delimiter_validation @format_check
Scenario Outline: Ensure delimiter consistency throughout the file
	Given a bank export file "<file_name>"
	When I check the delimiter format in the file
	Then the delimiter should be consistent throughout the file
		And mixed delimiters within the file should be flagged
		And an error report should be generated listing inconsistent delimiters
Examples:
| file_name                              |
| bank_export_baseline_test.csv         |
| bank_export_baseline_test.xlsx        |
@delimiter_validation @mixed_delimiters @edge_case
Scenario Outline: Detect files with inconsistent delimiters
	Given a bank export file "<file_name>"
	When I check the delimiter format in the file
	Then inconsistent delimiters such as mixed commas and semicolons should be detected
		And lines with incorrect delimiters should be logged separately
		And a suggestion should be provided to standardize delimiters
Examples:
| file_name                              |
| bank_export_mixed_delimiters_test.csv |
| bank_export_mixed_delimiters_test.xlsx |
@delimiter_validation @delimiter_mismatch
Scenario Outline: Ensure files use the expected delimiter
	Given a bank export file "<file_name>"
	When I check the delimiter format in the file
	Then the file should use the expected delimiter "<expected_delimiter>"
		And files with a different delimiter should be flagged
		And a conversion option should be suggested
Examples:
| file_name                              | expected_delimiter |
| bank_export_comma_delimiter_test.csv  | ,                  |
| bank_export_semicolon_delimiter_test.xlsx | ;               |
@delimiter_validation @delimiter_malformed @corrupted_data
Scenario Outline: Detect malformed data caused by delimiter errors
	Given a bank export file "<file_name>"
	When I parse the file content
	Then malformed data due to incorrect delimiters should be identified
		And such records should be flagged for manual review
		And a structured log should list affected rows with recommended fixes
Examples:
| file_name                                |
| bank_export_malformed_delimiter_test.csv |
| bank_export_malformed_delimiter_test.xlsx |
@delimiter_validation @edge_case @large_files
Scenario Outline: Validate delimiter consistency in large files
	Given a bank export file "<file_name>"
	When I check the delimiter format in a file with more than 100,000 rows
	Then the delimiter should be consistent in all rows
		And inconsistent delimiters should be flagged for bulk correction
		And performance benchmarks should be recorded
Examples:
| file_name                                   |
| bank_export_large_file_delimiter_test.csv  |
| bank_export_large_file_delimiter_test.xlsx |
