@duplicate_tests @orphaned_transactions @export_comparison



Feature: Identify orphaned transactions (transactions without matching accounts)






@orphaned_transaction_check



Scenario: Ensure all transactions are linked to a valid account





	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system





12 I have a bank export file "bank_export_baseline_test.csv" from the new system



	When I compare transaction-account mappings





	Then no transactions should be orphaned





