@regression_tests @bug_fix_verification @export_comparison



Feature: Ensure previously resolved issues do not reoccur





@bug_fix_verification



Scenario: Validate that previous data export bugs do not reappear




	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system




12 I have a bank export file "bank_export_baseline_test.csv" from the new system



	When I execute the export file comparison




	Then no previously fixed data issues should reoccur




