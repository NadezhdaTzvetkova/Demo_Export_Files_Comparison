@data_validation @whitespace @export_comparison
Feature: Detect trailing and leading whitespace in fields

  @whitespace_check
  Scenario Outline: Ensure "<column>" values do not contain leading or trailing spaces
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
                And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I check the "<column>" column
    Then all values should be trimmed of whitespace

    Examples:
      | column             |
      | transaction_id     |
      | account_name       |
      | customer_name      |
      | merchant_name      |
