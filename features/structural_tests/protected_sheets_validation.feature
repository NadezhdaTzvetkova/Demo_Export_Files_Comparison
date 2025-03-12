@structural_tests @protected_sheets @export_comparison



Feature: Validate protected or locked Excel sheets






@protected_sheet_check



Scenario: Ensure locked sheets do not prevent data extraction in "bank_export_excel_protected_sheet_validation_params.xlsx"





	Given I have an Excel bank export file "bank_export_excel_protected_sheet_validation_params.xlsx"





	When I check for locked sheets





	Then all required data should be accessible for validation





