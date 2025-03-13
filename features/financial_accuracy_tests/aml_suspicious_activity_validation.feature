@aml_compliance @suspicious_transactions
Scenario Outline: Detect suspicious AML transactions
	Given a bank export file "<file_name>"
	When I check the "Transaction Amount" and "Recipient" columns in "<sheet_name>"
	Then transactions above "<threshold>" should be flagged
		And flagged transactions should be reported to "<compliance_team>"
		And system should cross-check against known "<sanctioned_list>"
Examples:
| file_name                                | sheet_name | threshold | compliance_team    | sanctioned_list |
| bank_export_aml_large_transactions.csv  | N/A        | $10,000   | AML Compliance     | OFAC Watchlist |
| bank_export_suspicious_remittances.xlsx | Sheet1     | $50,000   | Financial Crimes   | EU Sanctions    |
