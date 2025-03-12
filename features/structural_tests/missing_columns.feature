@structural_tests @missing_columns @export_comparison
Feature: Detect missing columns in bank export files

  @missing_columns_check
  Scenario: Ensure missing columns are identified in "bank_export_missing_columns_test.xlsx" and "bank_export_missing_columns_test.csv"
    Given I have a bank export file "bank_export_missing_columns_test.xlsx" from the old system
    And I have a bank export file "bank_export_missing_columns_test.csv" from the new system
    When I compare the structure of both files
    Then I should identify the missing columns
