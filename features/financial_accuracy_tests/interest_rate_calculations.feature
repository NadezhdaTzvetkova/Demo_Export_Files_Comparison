@interest_rate @financial_accuracy
Scenario Outline: Validate correct interest calculations for loan payments
	Given a bank export file "<file_name>"
	When I check the "Interest Rate" and "Principal Amount" columns in "<sheet_name>"
	Then the calculated interest should match the expected formula "<formula>"
		And incorrect interest rates should be flagged
		And deviations greater than "<tolerance>" should trigger a compliance alert
Examples:
| file_name                            | sheet_name | formula             | tolerance |
| bank_export_loans_test.csv          | N/A        | (P * r * t)/100     | 0.01%     |
| bank_export_home_mortgage.xlsx      | Sheet1     | Compound Interest   | 0.05%     |
