@structural_tests @column_order @export_comparison
Feature: Validate handling of reordered columns in bank export files

  @column_order_check
  Scenario: Ensure column reordering does not affect validation in "bank_export_reordered_columns_test.xlsx" and "bank_export_reordered_columns_test.csv"
    Given I have a bank export file "bank_export_reordered_columns_test.xlsx" from the old system
    And I have a bank export file "bank_export_reordered_columns_test.csv" from the new system
    When I compare the structure of both files
    Then column reordering should not cause mismatches
