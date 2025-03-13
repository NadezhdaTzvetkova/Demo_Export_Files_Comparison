@capital_requirements @financial_compliance
Scenario Outline: Validate Basel III capital adequacy reports
	Given a bank export file "<file_name>"
	When I check the "Tier 1 Capital", "Risk-Weighted Assets", and "Capital Ratio" fields in "<sheet_name>"
	Then all values should match the Basel III calculation formula "<formula>"
		And reports failing to meet "<capital_threshold>" should be flagged for regulatory review
Examples:
| file_name                            | sheet_name | formula                  | capital_threshold |
| bank_export_basel_iii_report.csv    | N/A        | (Tier1 Capital / RWA)    | 8%                 |
| bank_export_liquidity_ratios.xlsx   | Sheet1     | LCR = HQLA / Net Outflow | 100%               |
