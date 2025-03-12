@data_validation @missing_values @export_comparison



Feature: Validate handling of missing values in export files




@missing_values_check



Scenario Outline: Ensure "<column>" correctly processes missing values in "bank_export_missing_values_test.xlsx" and "bank_export_missing_values_test.csv"



Given I have a bank export file "bank_export_missing_values_test.xlsx" from the old system



	And I have a bank export file "bank_export_missing_values_test.csv" from the new system



When I check the "<column>" column



Then missing values should be handled properly




Examples:



| column             |



| transaction_id     |



| transaction_amount |



| currency           |



| account_number     |



