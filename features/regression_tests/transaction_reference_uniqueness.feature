@regression_tests @transaction_reference_uniqueness @export_comparison
Feature: Validate transaction reference uniqueness
@unique_transaction_references
Scenario: Ensure all transaction references are unique
	Given I have a bank export file "bank_export_excel_transaction_reference_uniqueness_validation_params.xlsx"
		And I have a bank export file "bank_export_csv_transaction_reference_uniqueness_validation_params.csv"
	When I compare transaction reference numbers
	Then no duplicate transaction references should exist
