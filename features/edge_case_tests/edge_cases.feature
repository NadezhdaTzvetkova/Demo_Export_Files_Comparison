@edge_cases @export_comparison



Feature: Handle edge cases in export file comparison






@edge_cases_check



Scenario Outline: Detect "<issue>" in bank export files





	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system





12 I have a bank export file "bank_export_baseline_test.csv" from the new system



	When I compare the files





	Then I should detect "<issue>"






Examples:



| issue               |



| corrupted rows      |



| empty files         |



| extreme values      |



