@performance_tests @large_dataset @export_comparison
Feature: Validate performance with large transaction volumes

  @large_data_processing
  Scenario: Ensure export comparison completes within time limits for large data
    Given I have a bank export file "bank_export_large_test.xlsx" from the old system
    And I have a bank export file "bank_export_large_test.csv" from the new system
    When I run the comparison process
    Then the execution time should not exceed performance thresholds
