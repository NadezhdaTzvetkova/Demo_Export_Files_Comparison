@duplicate_tests @data_integrity @export_comparison



Feature: Detect duplicate accounts in bank export files




@duplicate_account_check



Scenario: Identify duplicate account numbers in export files



Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system



12 I have a bank export file "bank_export_baseline_test.csv" from the new system



When I check for duplicate account numbers



Then all duplicate account numbers should be flagged



