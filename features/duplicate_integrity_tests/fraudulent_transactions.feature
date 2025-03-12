@duplicate_tests @fraud_detection @export_comparison
Feature: Detect fraudulent or flagged transactions

@fraudulent_transaction_check
Scenario: Ensure all flagged transactions are identified

	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system

		And I have a bank export file "bank_export_baseline_test.csv" from the new system

	When I check for fraud indicators in transactions

	Then all fraudulent transactions should be flagged

