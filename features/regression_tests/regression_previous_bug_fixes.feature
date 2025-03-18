Feature: Validate Previously Fixed Bugs in Regression Testing
@regression_tests @previous_bug_fixes @data_integrity
Scenario Outline: Ensure previously fixed data-related issues do not reoccur
	Given a bank export file named "<file_name>" that had an issue fixed in version "<fixed_version>"
	When I process the file
	Then the issue should not reoccur
		And a validation report should confirm the resolution
		And any unexpected reappearance should be logged as "<severity>"
Examples:
| file_name                  | fixed_version | severity  |
| transactions_2021.csv      | v1.2.3       | High      |
| transactions_2023.xlsx     | v2.5.1       | Medium    |
@regression_tests @previous_bug_fixes @database_consistency
Scenario Outline: Validate database consistency for previously fixed issues
	Given a database that contained records affected by "<issue_type>"
	When I compare the latest records with the resolved state
	Then no past issues should reappear
		And any detected inconsistencies should be logged as "<discrepancy_type>"
		And alerts should be generated for critical regressions
Examples:
| issue_type             | discrepancy_type  |
| Duplicate Transactions | Unexpected Duplicates |
| Invalid Currencies     | Non-standard Codes  |
@regression_tests @previous_bug_fixes @batch_processing
Scenario Outline: Ensure batch processing maintains resolved bug fixes
	Given a batch of bank export files from "<year_range>" containing previously flagged issues
	When I process them for validation
	Then all records should pass consistency checks
		And no previously fixed issues should reoccur
		And any detected issues should be flagged as "<severity>"
Examples:
| year_range     | severity  |
| 2018 - 2022   | High      |
| 2023 - 2024   | Medium    |
@regression_tests @previous_bug_fixes @error_handling
Scenario Outline: Verify proper error handling for regression of resolved issues
	Given an attempt to process a bank export file "<file_name>"
	When a previously fixed issue such as "<error_type>" is detected again
	Then a system alert should notify relevant users
		And the issue should be escalated if its severity level is "<severity_level>"
		And a historical report should be updated with the reoccurrence
Examples:
| file_name                | error_type               | severity_level |
| transactions_2019.csv    | Corrupted Data Reentry  | High           |
| transactions_2021.xlsx   | Unexpected Null Values  | Medium         |
@regression_tests @previous_bug_fixes @performance_testing
Scenario Outline: Evaluate performance impact of verifying previously resolved issues
	Given a system processing "<file_count>" bank export files per hour
	When checking for previously fixed issues in "<year_range>"
	Then processing should complete within "<expected_time>" seconds
		And system resources should not exceed "<resource_limit>%"
		And data integrity should remain stable throughout the process
Examples:
| file_count | year_range     | expected_time | resource_limit |
| 100       | 2015 - 2020    | 300           | 70            |
| 500       | 2021 - 2023    | 600           | 80            |
