@performance_tests @concurrent_processing @export_comparison



Feature: Validate concurrent processing of large export files






@concurrent_processing_check



Scenario: Ensure concurrent processing does not cause data corruption





	Given I have a large bank export file "bank_export_large_test.xlsx" from the old system





12 I have a large bank export file "bank_export_large_test.csv" from the new system



	When multiple processes access these files simultaneously





	Then data should not be corrupted





