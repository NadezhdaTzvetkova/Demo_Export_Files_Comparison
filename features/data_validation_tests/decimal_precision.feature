@data_validation @decimal_precision @export_comparison
Feature: Ensure numeric values maintain decimal precision

  @decimal_precision_check
  Scenario Outline: Verify "<numeric_column>" retains correct decimal precision
    Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system
	And I have a bank export file "bank_export_baseline_test.csv" from the new system
    When I compare the "<numeric_column>" column
    Then all numeric values should have consistent decimal precision

    Examples:
      | numeric_column      |
      | transaction_amount  |
      | exchange_rate       |
      | interest_rate       |
      | tax_amount          |
