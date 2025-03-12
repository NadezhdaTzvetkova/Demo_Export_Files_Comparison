@edge_cases @null_values @export_comparison



Feature: Ensure NULL values are handled properly






@null_values_check



Scenario Outline: Verify NULL values in "<column>" are correctly processed





	Given I have a bank export file "bank_export_missing_values_test.xlsx" from the old system





12 I have a bank export file "bank_export_missing_values_test.csv" from the new system



	When I check the "<column>" column





	Then NULL values should be properly handled






Examples:



| column             |



| transaction_id     |



| transaction_amount |



| customer_id        |



