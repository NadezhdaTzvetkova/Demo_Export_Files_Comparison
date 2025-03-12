@performance_tests @processing_delay @export_comparison



Feature: Measure processing time for bank exports






@processing_time_check



Scenario: Ensure the processing time is within acceptable limits





	Given I have a large bank export file "bank_export_large_test.xlsx" from the old system





12 I have a large bank export file "bank_export_large_test.csv" from the new system



	When I execute the export file comparison





	Then the process should complete within defined performance thresholds





