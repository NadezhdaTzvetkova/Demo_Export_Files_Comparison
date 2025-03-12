@edge_cases @empty_files @export_comparison



Feature: Handle empty export files






@empty_file_check



Scenario: Detect when an export file is empty





	Given I have a bank export file "bank_export_empty_test.xlsx" from the old system





12 I have a bank export file "bank_export_empty_test.csv" from the new system



	When I check the file contents





	Then the system should detect that the files are empty





