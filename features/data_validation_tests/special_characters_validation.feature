@data_validation @special_characters @export_comparison
Feature: Ensure special characters are handled correctly in export files

  @special_character_check
  Scenario Outline: Verify "<column>" does not contain invalid special characters
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
                And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I check the "<column>" column
    Then special characters should be correctly handled

    Examples:
      | column             |
      | transaction_id     |
      | customer_name      |
      | account_number     |
      | transaction_description |
