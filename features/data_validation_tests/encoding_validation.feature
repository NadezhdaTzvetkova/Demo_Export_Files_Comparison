Feature: Validate Encoding Consistency
@encoding_validation @format_check
Scenario Outline: Ensure file encoding is UTF-8 or ASCII
	Given a bank export file "<file_name>"
	When I check the file encoding
	Then the file encoding should be "UTF-8" or "ASCII"
		And non-standard encodings should be flagged
		And the system should suggest converting to a standard encoding
Examples:
| file_name                              |
| bank_export_baseline_test.csv         |
| bank_export_baseline_test.xlsx        |
@encoding_validation @non_utf8_encoding @edge_case
Scenario Outline: Detect files with non-UTF-8 encoding
	Given a bank export file "<file_name>"
	When I check the file encoding
	Then files encoded in "ISO-8859-1" or other non-UTF-8 formats should be flagged
		And conversion options should be suggested
		And encoding-related errors should be logged
Examples:
| file_name                              |
| bank_export_non_utf8_encoding_test.csv |
| bank_export_non_utf8_encoding_test.xlsx |
@encoding_validation @invalid_characters
Scenario Outline: Detect invalid characters due to encoding issues
	Given a bank export file "<file_name>"
	When I scan the file for encoding errors
	Then non-printable or special characters should be flagged
		And invalid characters should be replaced or removed as per system policy
		And an error report should be generated
Examples:
| file_name                               |
| bank_export_invalid_characters_test.csv |
| bank_export_invalid_characters_test.xlsx |
@encoding_validation @mixed_encodings @corrupted_data
Scenario Outline: Detect mixed encoding formats within a single file
	Given a bank export file "<file_name>"
	When I check the encoding format of each row
	Then rows with inconsistent encodings should be flagged
		And a structured log should list affected rows with recommended fixes
Examples:
| file_name                                  |
| bank_export_mixed_encoding_test.csv       |
| bank_export_mixed_encoding_test.xlsx      |
@encoding_validation @edge_case @large_files
Scenario Outline: Validate encoding consistency in large files
	Given a bank export file "<file_name>"
	When I check the encoding format in a file with more than 100,000 rows
	Then encoding should be consistent across all rows
		And inconsistencies should be flagged for bulk correction
		And performance benchmarks should be recorded
Examples:
| file_name                                    |
| bank_export_large_file_encoding_test.csv    |
| bank_export_large_file_encoding_test.xlsx   |
