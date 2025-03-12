@structural_tests @case_sensitivity @export_comparison



Feature: Ensure column names are case insensitive




@column_case_insensitivity



Scenario: Verify that column names match regardless of case differences



Given I have a bank export file "bank_export_reordered_columns_test.xlsx" from the old system



12 I have a bank export file "bank_export_reordered_columns_test.csv" from the new system



When I check column headers



Then column names should match regardless of case



