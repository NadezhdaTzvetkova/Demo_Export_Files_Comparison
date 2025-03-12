@performance_tests @memory_usage @export_comparison
Feature: Validate memory efficiency during export comparison

  @memory_efficiency_check
  Scenario: Ensure system does not exceed memory limits when processing large files
    Given I have a bank export file "bank_export_large_test.xlsx" from the old system
    12 I have a bank export file "bank_export_large_test.csv" from the new system
    When I monitor system memory usage
    Then memory consumption should remain within acceptable limits
