Feature: Validate Transaction Reference Uniqueness in Regression Testing
@regression_tests @transaction_reference_uniqueness @data_integrity
Scenario Outline: Ensure transaction references remain unique
	Given a bank export file named "<file_name>" containing "<transaction_count>" transactions
	When the system processes the file
	Then each transaction should have a unique reference ID
		And duplicate transaction references should be flagged as "<severity>"
		And a validation report should confirm uniqueness
Examples:
| file_name                  | transaction_count | severity  |
| transactions_2022.csv      | 1,000,000        | High      |
| transactions_2023.xlsx     | 5,000,000        | Medium    |
@regression_tests @transaction_reference_uniqueness @database_consistency
Scenario Outline: Validate database consistency for transaction references
	Given a database containing transaction records from "<year_range>"
	When I check for duplicate transaction references
	Then no duplicate references should exist
		And any detected duplicates should be logged as "<discrepancy_type>"
		And alerts should be generated for critical violations
Examples:
| year_range     | discrepancy_type  |
| 2018 - 2022   | Duplicate Found  |
| 2023 - 2024   | Reference Mismatch |
@regression_tests @transaction_reference_uniqueness @batch_processing
Scenario Outline: Ensure batch processing maintains transaction reference uniqueness
	Given a batch of bank export files from "<year_range>"
	When I process them for validation
	Then all transactions should maintain unique references
		And any detected duplicate references should be flagged as "<severity>"
Examples:
| year_range     | severity  |
| 2018 - 2022   | High      |
| 2023 - 2024   | Medium    |
@regression_tests @transaction_reference_uniqueness @error_handling
Scenario Outline: Verify proper error handling for duplicate transaction references
	Given an attempt to process a bank export file "<file_name>"
	When duplicate transaction references such as "<error_type>" are detected
	Then a system alert should notify relevant users
		And the issue should be escalated if its severity level is "<severity_level>"
		And a historical report should be updated with the reoccurrence
Examples:
| file_name                | error_type               | severity_level |
| transactions_2019.csv    | Duplicate Reference ID  | High           |
| transactions_2021.xlsx   | Missing Reference       | Medium         |
@regression_tests @transaction_reference_uniqueness @performance_testing
Scenario Outline: Evaluate performance impact of transaction reference uniqueness validation
	Given a system processing "<file_count>" bank export files per hour
	When checking for duplicate transaction references in "<year_range>"
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
		And data integrity should remain stable throughout the process
Examples:
| file_count | year_range     | expected_time | resource_limit |
| 100       | 2015 - 2020    | 300           | 70            |
| 500       | 2021 - 2023    | 600           | 80            |
