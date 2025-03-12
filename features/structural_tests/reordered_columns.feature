Feature: Validate Handling of Reordered Columns in Structural Testing
@structural_tests @reordered_columns @data_integrity
Scenario Outline: Ensure reordered columns are detected and realigned
	Given a bank export file "<file_name>" with columns in an unexpected order
	When the system processes the file
	Then column order should be verified against the reference format "<reference_file>"
		And any reordering should be flagged as "<severity>"
		And if auto-mapping is enabled, the system should realign the columns
Examples:
| file_name                         | reference_file                        | severity  |
| transactions_reordered.csv         | transactions_standard.csv              | High      |
| transactions_reordered.xlsx        | transactions_standard.xlsx             | Medium    |
| transactions_partial_reorder.xlsx  | transactions_standard_partial.xlsx     | Low       |
@structural_tests @reordered_columns @error_handling
Scenario Outline: Validate error handling for reordered columns
	Given an attempt to process a bank export file "<file_name>"
	When columns are reordered in an unexpected way
	Then a system alert should notify relevant users
		And the issue should be escalated if the severity level is "<severity_level>"
		And if auto-mapping is available, a correction suggestion should be provided
		And if auto-mapping fails, the file should be flagged for manual review
Examples:
| file_name                        | severity_level |
| transactions_2020_reordered.csv  | High           |
| transactions_2021_reordered.xlsx | Medium         |
| transactions_test_reorder.xlsx   | Low            |
@structural_tests @reordered_columns @batch_processing
Scenario Outline: Ensure batch processing handles reordered columns correctly
	Given a batch of bank export files with reordered columns
	When the system processes them for validation
	Then all column order discrepancies should be detected and flagged as "<severity>"
		And processing should continue without failure
		And misaligned files should be logged separately for further review
Examples:
| severity  |
| High      |
| Medium    |
| Low       |
@structural_tests @reordered_columns @performance_testing
Scenario Outline: Evaluate performance impact of reordered column validation
	Given a system processing "<file_count>" bank export files per hour
	When reordered columns are present in "<year_range>"
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
		And column integrity should be maintained throughout the process
Examples:
| file_count | year_range     | expected_time | resource_limit |
| 100        | 2015 - 2020    | 300           | 70            |
| 500        | 2021 - 2023    | 600           | 80            |
@structural_tests @reordered_columns @schema_validation
Scenario Outline: Validate system behavior for schema mismatches due to reordered columns
	Given an export file "<file_name>" with schema "<schema_type>"
	When I check the schema validation rules
	Then reordered columns should be flagged as "<error_severity>"
		And system logs should capture all schema-related discrepancies
		And if possible, column mappings should be suggested to match "<expected_format>"
Examples:
| file_name                    | schema_type       | expected_format    | error_severity |
| transactions_legacy.csv       | Legacy Format    | Standard V1.2      | High           |
| transactions_modified.xlsx    | Custom Schema    | Standard V1.3      | Medium         |
| transactions_test.csv         | Test Environment | Test Format V2.0   | Low            |
@structural_tests @reordered_columns @referential_integrity
Scenario Outline: Ensure referential integrity is maintained despite reordered columns
	Given a bank export file "<file_name>" with reordered columns
	When I compare "<column_name>" values across reference data
	Then referential integrity should not be broken
		And mismatches should be logged as "<severity>"
Examples:
| file_name                     | column_name         | severity  |
| transactions_reordered.csv     | Account Number      | High      |
| transactions_partial_reorder.xlsx | Transaction ID   | Medium    |
@structural_tests @reordered_columns @auto_mapping
Scenario Outline: Validate auto-mapping for reordered columns
	Given a system with auto-mapping enabled
	When processing a file "<file_name>" with reordered columns
	Then the system should attempt to realign the columns based on "<reference_file>"
		And if realignment fails, the issue should be flagged as "<severity>"
Examples:
| file_name                         | reference_file                 | severity  |
| transactions_reordered.csv         | transactions_standard.csv       | High      |
| transactions_reordered.xlsx        | transactions_standard.xlsx      | Medium    |
@structural_tests @reordered_columns @data_consistency
Scenario Outline: Ensure reordered columns do not impact data consistency
	Given a bank export file "<file_name>"
	When I compare "<column_name>" values between the legacy and migrated system
	Then all values should remain identical despite column reordering
		And data consistency should be maintained across all rows
Examples:
| file_name                     | column_name         |
| transactions_reordered.csv     | Account Number      |
| transactions_partial_reorder.xlsx | Transaction ID   |
@structural_tests @reordered_columns @memory_usage_validation
Scenario Outline: Validate memory and CPU usage when handling reordered columns
	Given a system processing "<file_count>" large files with reordered columns
	When the validation system runs
	Then the memory usage should not exceed "<max_memory_usage> MB"
		And processing should complete within "<expected_time>" seconds
Examples:
| file_count | max_memory_usage | expected_time |
| 500        | 512              | 300           |
| 1000       | 1024             | 600           |
@structural_tests @reordered_columns @delimiter_consistency
Scenario Outline: Ensure column reordering does not break delimiter consistency
	Given a CSV file "<file_name>" with columns reordered near delimiters
	When the system parses the file
	Then delimiter integrity should be preserved
		And no columns should shift due to unexpected order
Examples:
| file_name                           |
| transactions_reordered_delimiters.csv |
| transactions_misaligned_delim.csv    |
