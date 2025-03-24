Feature: Tax Withholding Validation
@financial_accuracy @tax_withholding @compliance

Scenario Outline: Ensure correct tax withholding percentage
	Given a bank export file "<file_name>"
	When I check the "Tax Withheld" column in the "<sheet_name>" sheet
	Then all tax withholdings should be "<expected_tax_rate>%"
	And discrepancies should be flagged for review
	And incorrect tax rates should be escalated for compliance audit


Examples:
| file_name                               | sheet_name | expected_tax_rate |
| tax_withholding_standard_test.csv      | N/A        | 15.00%            |
| tax_withholding_standard_test.xlsx     | Sheet1     | 15.00%            |
@financial_accuracy @tax_compliance @edge_case

Scenario Outline: Detect tax withholding anomalies
	Given a bank export file "<file_name>"
	When I check the "Tax Withheld" column in the "<sheet_name>" sheet
	Then negative or missing tax amounts should be flagged
	And unusually high or low tax rates should be reported


Examples:
| file_name                               | sheet_name |
| tax_withholding_anomalies_test.csv     | N/A        |
| tax_withholding_anomalies_test.xlsx    | Sheet1     |
