@duplicate_tests @customer_duplicates @export_comparison
Feature: Detect duplicate customer records in bank export files

  @duplicate_customer_check
  Scenario: Identify duplicate customer records
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
    And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I check for duplicate customer records
    Then all duplicate customers should be flagged
