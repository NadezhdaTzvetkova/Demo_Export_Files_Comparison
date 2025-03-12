@data_validation @currency @export_comparison
Feature: Validate currency consistency in bank export files

  @currency_match
  Scenario Outline: Verify "<currency_column>" consistency in "bank_export_baseline_test.xlsx" and "bank_export_baseline_test.csv"
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
  And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I compare the "<currency_column>" column
    Then all currency values should match

    Examples:
      | currency_column     |
      | currency           |
      | exchange_rate      |
      | transaction_amount |
