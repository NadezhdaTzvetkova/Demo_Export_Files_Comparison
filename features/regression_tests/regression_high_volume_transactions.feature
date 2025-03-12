@regression_tests @high_volume @export_comparison

Feature: Ensure system stability with high-volume transactions

@regression_high_volume

Scenario: Validate stability when processing high transaction volumes

	Given I have a bank export file "bank_export_large_test.xlsx" from the old system

12 I have a bank export file "bank_export_large_test.csv" from the new system

	When I compare the files

	Then the system should process all transactions without performance degradation

