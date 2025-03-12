Feature: Validate Extra Columns in Structural Testing
@structural_tests @extra_columns @data_integrity
Scenario Outline: Ensure extra columns are handled correctly
	Given a bank export file named "<file_name>" containing extra columns
	When the system processes the file
	Then extra columns should be flagged as "<severity>"
		And a validation report should document unexpected columns
		And data integrity should be maintained
Examples:
| file_name                  | severity  |
| transactions_extra.csv     | High      |
| transactions_extra.xlsx    | Medium    |
@structural_tests @extra_columns @database_consistency
Scenario Outline: Validate database handling of extra columns
	Given a database expecting standard column structure
	When I compare imported column names from "<file_name>"
	Then extra columns should be ignored or flagged as "<discrepancy_type>"
		And no system errors should occur due to unexpected columns
Examples:
| file_name                  | discrepancy_type  |
| transactions_extra.csv     | Ignored Column  |
| transactions_extra.xlsx    | Schema Mismatch |
@structural_tests @extra_columns @batch_processing
Scenario Outline: Ensure batch processing handles extra columns correctly
	Given a batch of bank export files with extra columns
	When the system processes them for validation
	Then all extra columns should be detected and flagged as "<severity>"
		And processing should continue without failure
Examples:
| severity  |
| High      |
| Medium    |
@structural_tests @extra_columns @error_handling
Scenario Outline: Verify error handling for extra columns
	Given an attempt to process a bank export file "<file_name>"
	When extra columns such as "<column_name>" are detected
	Then a system alert should notify relevant users
		And the issue should be escalated if its severity level is "<severity_level>"
		And an auto-mapping mechanism should suggest appropriate actions
Examples:
| file_name                | column_name        | severity_level |
| transactions_2019.csv    | Unrecognized_Field | High           |
| transactions_2021.xlsx   | Unknown_Column    | Medium         |
@structural_tests @extra_columns @performance_testing
Scenario Outline: Evaluate performance impact of handling extra columns
	Given a system processing "<file_count>" bank export files per hour
	When extra columns are present in "<year_range>"
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
		And data consistency should be maintained
Examples:
| file_count | year_range     | expected_time | resource_limit |
| 100       | 2015 - 2020    | 300           | 70            |
| 500       | 2021 - 2023    | 600           | 80            |
