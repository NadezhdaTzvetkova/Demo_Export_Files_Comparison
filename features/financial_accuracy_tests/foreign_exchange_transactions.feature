@fx_transactions @currency_conversion
Scenario Outline: Validate exchange rates for foreign currency transactions
	Given a bank export file "<file_name>"
	When I check the "Currency", "Amount", and "Exchange Rate" columns in "<sheet_name>"
	Then the converted amount should match official exchange rates within "<tolerance>"
		And transactions exceeding "<alert_threshold>" should trigger a compliance review
Examples:
| file_name                               | sheet_name | tolerance | alert_threshold |
| bank_export_foreign_transactions.csv   | N/A        | 0.5%      | $50,000         |
| bank_export_high_risk_forex.xlsx      | Sheet1     | 0.3%      | $100,000        |
