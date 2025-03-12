@data_integrity @transaction_mismatch @export_comparison
Feature: Detect mismatched transaction records

  @transaction_mismatch_check
  Scenario: Identify transactions present in one export file but missing in the other
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
    And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I compare all transaction records
    Then I should detect transactions that are missing in either file
