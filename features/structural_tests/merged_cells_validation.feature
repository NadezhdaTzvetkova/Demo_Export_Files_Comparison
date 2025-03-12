@structural_tests @merged_cells @export_comparison
Feature: Validate merged cells in Excel exports
@merged_cells_check
Scenario: Ensure merged cells do not affect data integrity in "bank_export_excel_merged_cells_validation_params.xlsx"
	Given I have an Excel bank export file "bank_export_excel_merged_cells_validation_params.xlsx"
	When I check for merged cells
	Then merged cells should not cause incorrect data interpretation
