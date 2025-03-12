@regression_tests @duplicate_imports @export_comparison

Feature: Detect duplicate file imports in export comparison

@duplicate_imports_check

Scenario: Ensure duplicate files are flagged when re-imported

	Given I have a bank export file "bank_export_excel_duplicate_imports_validation_params.xlsx"

12 I have a bank export file "bank_export_csv_duplicate_imports_validation_params.csv"

	When I check for duplicate file imports

	Then no duplicate files should be processed again

