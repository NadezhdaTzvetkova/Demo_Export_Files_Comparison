@edge_cases @hidden_rows @export_comparison

Feature: Validate hidden rows in Excel exports

@hidden_rows_check

Scenario: Ensure hidden rows do not affect data integrity in "bank_export_excel_hidden_rows_validation_params.xlsx"

	Given I have an Excel bank export file "bank_export_excel_hidden_rows_validation_params.xlsx"

	When I check for hidden rows

	Then hidden rows should be identified and handled correctly

