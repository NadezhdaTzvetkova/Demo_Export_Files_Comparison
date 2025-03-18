Feature: Validate Handling of Missing Columns in Structural Testing
@structural_tests @missing_columns @data_integrity
Scenario Outline: Ensure missing columns are detected and flagged
	Given a bank export file named "<file_name>" with missing columns "<missing_columns>"
	When the system processes the file
	Then the missing columns should be flagged with severity "<severity>"
		And a validation report should document the missing fields
		And if auto-mapping is enabled, a correction suggestion should be provided
Examples:
| file_name                          | missing_columns       | severity  |
| transactions_missing_account.csv   | Account Number        | High      |
| transactions_missing_currency.xlsx | Currency Code         | Medium    |
| transactions_partial_missing.csv   | Date, Transaction ID  | High      |
@structural_tests @missing_columns @error_handling
Scenario Outline: Validate error handling for missing columns
	Given an attempt to process a bank export file "<file_name>"
	When required columns are missing such as "<missing_column>"
	Then a system alert should notify relevant users
		And the issue should be escalated if the missing column severity level is "<severity_level>"
		And an auto-mapping mechanism should suggest appropriate corrections if applicable
		And if correction is not possible, the file should be rejected
Examples:
| file_name                           | missing_column       | severity_level |
| transactions_2019.csv               | Transaction ID       | High           |
| transactions_2021.xlsx              | Amount              | Medium         |
| transactions_with_gaps.xlsx         | Date, Account Number | High           |
@structural_tests @missing_columns @batch_processing
Scenario Outline: Ensure batch processing handles missing columns correctly
	Given a batch of bank export files with missing columns
	When the system processes them for validation
	Then all missing column occurrences should be detected and flagged as "<severity>"
		And processing should continue without failure
		And incorrectly formatted files should be logged separately for further review
Examples:
| severity  |
| High      |
| Medium    |
| Low       |
@structural_tests @missing_columns @performance_testing
Scenario Outline: Evaluate performance impact of missing column validation
	Given a system processing "<file_count>" bank export files per hour
	When missing columns are present in "<year_range>"
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
		And data integrity should be maintained throughout the process
Examples:
| file_count | year_range     | expected_time | resource_limit |
| 100        | 2015 - 2020    | 300           | 70            |
| 500        | 2021 - 2023    | 600           | 80            |
@structural_tests @missing_columns @schema_validation
Scenario Outline: Validate system behavior for schema mismatches due to missing columns
	Given an export file "<file_name>" with schema "<schema_type>"
	When I check the schema validation rules
	Then missing columns should be flagged as "<error_severity>"
		And system logs should capture all schema-related discrepancies
Examples:
| file_name                    | schema_type       | error_severity |
| transactions_legacy.csv       | Legacy Format    | High           |
| transactions_modified.xlsx    | Custom Schema    | Medium         |
| transactions_test.csv         | Test Environment | Low            |
