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
@financial_accuracy @interest_rates @format_check
Scenario Outline: Ensure correct interest rate format in exports
	Given a bank export file "<file_name>"
	When I check the "Interest Rate" column in the "<sheet_name>" sheet
	Then all interest rates should be formatted correctly as "<expected_format>"
		And interest rates should be expressed as a percentage with up to two decimal places
		And values exceeding regulatory limits should be flagged
Examples:
| file_name                                  | sheet_name | expected_format |
| bank_export_baseline_test.csv             | N/A        | X.XX%           |
| bank_export_baseline_test.xlsx            | Sheet1     | X.XX%           |
| bank_export_high_interest_rates_test.csv  | N/A        | X.XX%           |
| bank_export_high_interest_rates_test.xlsx | Sheet1     | X.XX%           |
@financial_accuracy @interest_calculation @edge_case
Scenario Outline: Validate daily vs. monthly interest calculations
	Given a bank export file "<file_name>"
	When I compare "Daily Interest" and "Monthly Interest" calculations in the "<sheet_name>" sheet
	Then calculated interest should match expected values based on "<interest_formula>"
		And rounding differences should not exceed "<rounding_tolerance>"
		And discrepancies beyond tolerance should be logged for review
Examples:
| file_name                                   | sheet_name | interest_formula | rounding_tolerance |
| bank_export_interest_calculations_test.csv | N/A        | Principal * Rate / 365 | 0.01 |
| bank_export_interest_calculations_test.xlsx | Sheet1     | Principal * Rate / 12  | 0.01 |
@financial_accuracy @compounding_interest @loan_validation
Scenario Outline: Ensure correct compounding interest application
	Given a bank export file "<file_name>"
	When I check the "Compounded Interest" column in the "<sheet_name>" sheet
	Then all values should match the calculated interest for "<compounding_period>"
		And rounding rules should follow regulatory guidelines
		And discrepancies should be flagged for review
Examples:
| file_name                                  | sheet_name | compounding_period |
| bank_export_compound_interest_test.csv    | N/A        | Daily              |
| bank_export_compound_interest_test.xlsx   | Sheet1     | Monthly            |
| bank_export_compound_interest_test.xlsx   | Sheet2     | Quarterly          |
