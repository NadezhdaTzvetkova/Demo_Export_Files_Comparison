@performance_tests @high_concurrency @export_comparison
Feature: Validate performance under high concurrent users

  @high_concurrency_check
  Scenario: Ensure the system handles multiple users processing exports simultaneously
    Given multiple users are comparing export files concurrently
    When I compare "bank_export_large_test.xlsx" and "bank_export_large_test.csv"
    Then the system should not experience performance degradation
