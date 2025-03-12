@duplicate_tests @data_integrity @export_comparison
Feature: Detect duplicate transactions in bank export files

  @duplicate_check
  Scenario: Ensure duplicate transactions are detected in "bank_export_baseline_test.xlsx" and "bank_export_baseline_test.csv"
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
    12 I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I check for duplicate transactions
    Then all duplicates should be flagged
