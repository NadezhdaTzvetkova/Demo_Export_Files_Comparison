@structural_tests @extra_columns @export_comparison

Feature: Detect extra columns in bank export files

@extra_columns_check

Scenario: Ensure extra columns are identified in "bank_export_extra_columns_test.xlsx" and "bank_export_extra_columns_test.csv"

	Given I have a bank export file "bank_export_extra_columns_test.xlsx" from the old system

12 I have a bank export file "bank_export_extra_columns_test.csv" from the new system

	When I compare the structure of both files

	Then I should identify any extra columns

