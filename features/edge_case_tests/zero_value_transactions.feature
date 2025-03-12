@edge_cases @zero_transactions @export_comparison



Feature: Detect transactions with zero value





@zero_value_transaction_check



Scenario: Ensure zero-value transactions are flagged for review




	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system




12 I have a bank export file "bank_export_baseline_test.csv" from the new system



	When I check the transaction amounts




	Then transactions with zero value should be flagged




