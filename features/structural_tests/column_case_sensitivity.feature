Feature: Validate Column Case Sensitivity in Structural Testing
@structural_tests @column_case_sensitivity @data_integrity
Scenario Outline: Ensure column names are correctly recognized despite case variations
	Given a bank export file named "<file_name>" with columns in "<case_format>"
	When the system processes the file
	Then column headers should be mapped correctly
		And no data should be lost due to case mismatches
		And a validation report should confirm column integrity
Examples:
| file_name                | case_format    |
| transactions_lower.csv   | lowercase      |
| transactions_UPPER.xlsx  | uppercase      |
| transactions_MiXeD.csv   | mixed_case     |
@structural_tests @column_case_sensitivity @database_consistency
Scenario Outline: Validate database column mappings for different case formats
	Given a database with expected column names in "<expected_case_format>"
	When I compare imported column names from "<file_name>"
	Then column mappings should be case-insensitive
		And any discrepancies should be logged as "<discrepancy_type>"
		And alerts should be generated for critical inconsistencies
Examples:
| file_name                | expected_case_format | discrepancy_type  |
| transactions_lower.csv   | Title Case          | Column Not Found  |
| transactions_UPPER.xlsx  | Lowercase           | Case Mismatch     |
@structural_tests @column_case_sensitivity @batch_processing
Scenario Outline: Ensure batch processing maintains correct column case mapping
	Given a batch of bank export files with columns in "<case_format>"
	When the system processes them for validation
	Then all columns should be correctly recognized
		And no data loss should occur due to case variations
		And any detected mismatches should be flagged as "<severity>"
Examples:
| case_format   | severity  |
| lowercase     | High      |
| uppercase     | Medium    |
| mixed_case    | Low       |
@structural_tests @column_case_sensitivity @error_handling
Scenario Outline: Verify error handling for column case mismatches
	Given an attempt to process a bank export file "<file_name>"
	When a column case mismatch such as "<error_type>" is detected
	Then a system alert should notify relevant users
		And the issue should be escalated if its severity level is "<severity_level>"
		And a correction mechanism should attempt to standardize column case
Examples:
| file_name                | error_type          | severity_level |
| transactions_2019.csv    | Missing Column      | High           |
| transactions_2021.xlsx   | Unrecognized Column | Medium         |
@structural_tests @column_case_sensitivity @performance_testing
Scenario Outline: Evaluate performance impact of case-insensitive column matching
	Given a system processing "<file_count>" bank export files per hour
	When checking for column case variations in "<year_range>"
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
		And column mappings should remain stable throughout the process
Examples:
| file_count | year_range     | expected_time | resource_limit |
| 100       | 2015 - 2020    | 300           | 70            |
| 500       | 2021 - 2023    | 600           | 80            |
