@data_validation @account_numbers @export_comparison
Feature: Validate correct formatting of account numbers

  @account_number_format
  Scenario Outline: Ensure "<account_column>" follows the correct format
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
    And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I validate the "<account_column>"
    Then all values should conform to the expected format

    Examples:
      | account_column  |
      | account_number  |
      | IBAN           |
      | SWIFT_code     |
      | routing_number |
