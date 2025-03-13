@aml_compliance @suspicious_transactions
Scenario Outline: Detect suspicious AML transactions
	Given a bank export file "<file_name>"
	When I check the "Transaction Amount" and "Recipient" columns in "<sheet_name>"
	Then transactions above "<threshold>" should be flagged
		And flagged transactions should be reported to "<compliance_team>"
		And system should cross-check against known "<sanctioned_list>"
Examples:
| file_name                                | sheet_name | threshold | compliance_team    | sanctioned_list  |
| bank_export_aml_large_transactions.csv  | N/A        | $10,000   | AML Compliance     | OFAC Watchlist  |
| bank_export_suspicious_remittances.xlsx | Sheet1     | $50,000   | Financial Crimes   | EU Sanctions    |
---
@aml_compliance @structured_transactions @fraud_detection
Scenario Outline: Detect structured transactions to evade AML reporting
	Given a bank export file "<file_name>"
	When I check multiple transactions in "<sheet_name>"
	Then transactions structured below "<threshold>" but summing above "<aggregate_limit>" should be flagged
		And such transactions should be linked to detect possible smurfing
		And flagged transactions should be reported for enhanced due diligence
Examples:
| file_name                               | sheet_name | threshold | aggregate_limit |
| bank_export_structured_payments.csv    | N/A        | $9,999    | $50,000         |
| bank_export_smurfing_patterns.xlsx     | Sheet1     | $1,000    | $20,000         |
---
@aml_compliance @high_risk_countries @geolocation_validation
Scenario Outline: Identify transactions involving high-risk jurisdictions
	Given a bank export file "<file_name>"
	When I check the "Sender Country" and "Recipient Country" in "<sheet_name>"
	Then transactions involving "<high_risk_country>" should be flagged
		And a report should be generated for AML compliance review
		And system should verify if the transaction aligns with expected customer behavior
Examples:
| file_name                               | sheet_name | high_risk_country |
| bank_export_sanctioned_country.csv    | N/A        | North Korea       |
| bank_export_high_risk_jurisdictions.xlsx | Sheet1     | Iran             |
---
@aml_compliance @unusual_behavior @transaction_patterns
Scenario Outline: Detect unusual customer behavior patterns
	Given a bank export file "<file_name>"
	When I analyze transaction history in "<sheet_name>"
	Then significant deviations from normal spending behavior should be flagged
		And alerts should be triggered for enhanced customer due diligence
		And flagged customers should be reviewed for AML risk scoring
Examples:
| file_name                            | sheet_name |
| bank_export_unusual_spending.csv    | N/A        |
| bank_export_customer_behavior.xlsx  | Sheet1     |
---
@aml_compliance @shell_company_detection @fraud_risk
Scenario Outline: Identify transactions linked to suspected shell companies
	Given a bank export file "<file_name>"
	When I cross-reference business accounts in "<sheet_name>" with known shell company lists
	Then transactions involving "<shell_company_name>" should be flagged
		And system should recommend enhanced verification for these entities
Examples:
| file_name                               | sheet_name | shell_company_name |
| bank_export_shell_company_transactions.csv  | N/A        | XYZ Offshore Ltd.  |
| bank_export_suspicious_entities.xlsx       | Sheet1     | ABC Holdings Inc.  |
---
@aml_compliance @large_cash_deposits @physical_branch
Scenario Outline: Flag large cash deposits made at physical branches
	Given a bank export file "<file_name>"
	When I check the "Transaction Type" and "Branch Location" in "<sheet_name>"
	Then cash deposits exceeding "<cash_threshold>" should be flagged
		And customers making such deposits should be reviewed for AML risk assessment
Examples:
| file_name                                 | sheet_name | cash_threshold |
| bank_export_large_cash_deposits.csv     | N/A        | $15,000       |
| bank_export_branch_activity.xlsx        | Sheet1     | $25,000       |
---
@aml_compliance @edge_case @large_files @performance
Scenario Outline: Validate AML transaction monitoring for large banking datasets
	Given a bank export file "<file_name>" with over "<row_count>" records
	When I check for AML compliance anomalies
	Then flagged transactions should be identified within "<expected_runtime>"
		And system performance should be optimized for large-scale fraud detection
Examples:
| file_name                              | row_count  | expected_runtime |
| bank_export_large_dataset_aml.csv      | 500,000    | 15 minutes       |
| bank_export_large_dataset_aml.xlsx     | 1,000,000  | 30 minutes       |
---
@aml_compliance @blacklisted_accounts @regulatory_watchlist
Scenario Outline: Detect transactions involving blacklisted individuals or entities
	Given a bank export file "<file_name>"
	When I cross-check "Account Holder" against "<watchlist>"
	Then transactions linked to blacklisted entities should be flagged
		And regulatory authorities should be notified for further investigation
Examples:
| file_name                               | sheet_name | watchlist         |
| bank_export_blacklisted_accounts.csv    | N/A        | FBI Watchlist     |
| bank_export_sanctions_list.xlsx         | Sheet1     | Interpol Red List |
@aml_compliance @cross_border_transactions @high_risk
Scenario Outline: Detect high-risk cross-border transactions
	Given a bank export file "<file_name>"
	When I analyze the "Sender Country", "Recipient Country", and "Transaction Amount" in "<sheet_name>"
	Then cross-border transactions exceeding "<threshold>" to "<high_risk_country>" should be flagged
		And the system should check for compliance with FATF regulations
		And a report should be generated for regulatory audit purposes
Examples:
| file_name                              | sheet_name | threshold | high_risk_country |
| bank_export_cross_border.csv          | N/A        | $50,000   | Russia           |
| bank_export_international_payments.xlsx | Sheet1     | $25,000   | Venezuela        |
---
@aml_compliance @cryptocurrency_transactions @fraud_detection
Scenario Outline: Monitor cryptocurrency-related transactions for fraud risk
	Given a bank export file "<file_name>"
	When I analyze the "Transaction Type" and "Recipient" fields in "<sheet_name>"
	Then transactions involving "<crypto_exchange>" should be flagged if above "<crypto_threshold>"
		And the system should check for potential money laundering activities
		And transactions should be reviewed against the FATF Travel Rule
Examples:
| file_name                              | sheet_name | crypto_exchange | crypto_threshold |
| bank_export_crypto_transactions.csv  | N/A        | Binance        | $10,000         |
| bank_export_blockchain_remittances.xlsx | Sheet1     | Coinbase       | $5,000          |
---
@aml_compliance @gdpr @privacy_violation @customer_data
Scenario Outline: Ensure AML reports comply with GDPR data privacy regulations
	Given a bank export file "<file_name>"
	When I check the fields containing personal customer data in "<sheet_name>"
	Then sensitive PII such as "Full Name", "SSN", and "Passport Number" should be anonymized
		And non-compliant records should be flagged for violation of GDPR Article 32
		And a data minimization report should be generated
Examples:
| file_name                              | sheet_name |
| bank_export_customer_data.csv         | N/A        |
| bank_export_personal_info.xlsx        | Sheet1     |
---
@aml_compliance @transaction_velocity @machine_learning
Scenario Outline: Detect abnormal transaction velocity using AI-based anomaly detection
	Given a bank export file "<file_name>"
	When I analyze transaction frequency per "<time_period>" for each account in "<sheet_name>"
	Then accounts exceeding "<velocity_threshold>" transactions per "<time_period>" should be flagged
		And flagged transactions should be reviewed for money laundering risk
		And risk assessment scores should be assigned to each flagged account
Examples:
| file_name                              | sheet_name | time_period | velocity_threshold |
| bank_export_high_freq_transactions.csv | N/A        | 24 hours    | 500                |
| bank_export_suspicious_activity.xlsx   | Sheet1     | 1 week      | 1,000              |
---
@aml_compliance @basel_iii @capital_reserve_validation
Scenario Outline: Ensure AML-related capital reserves meet Basel III requirements
	Given a bank export file "<file_name>"
	When I check the "Liquidity Coverage Ratio" and "Net Stable Funding Ratio" in "<sheet_name>"
	Then the calculated values should meet the Basel III minimum threshold of "<capital_threshold>"
		And any shortfall should be flagged for regulatory intervention
Examples:
| file_name                              | sheet_name | capital_threshold |
| bank_export_basel_iii_aml_compliance.csv | N/A        | 100%              |
| bank_export_liquidity_ratios.xlsx      | Sheet1     | 80%               |
---
@aml_compliance @unusual_large_withdrawals @risk_analysis
Scenario Outline: Identify unusually large cash withdrawals from high-risk customers
	Given a bank export file "<file_name>"
	When I check the "Transaction Type" and "Customer Risk Category" in "<sheet_name>"
	Then cash withdrawals above "<withdrawal_threshold>" from "<risk_category>" customers should be flagged
		And regulatory authorities should be alerted for risk-based assessment
Examples:
| file_name                                | sheet_name | withdrawal_threshold | risk_category  |
| bank_export_large_cash_withdrawals.csv | N/A        | $20,000             | Politically Exposed Person (PEP) |
| bank_export_high_risk_customers.xlsx  | Sheet1     | $50,000             | Offshore Business               |
---
@aml_compliance @fatf_sanctions @banking_regulation
Scenario Outline: Cross-check transactions against FATF and OFAC watchlists
	Given a bank export file "<file_name>"
	When I compare the "Sender Name" and "Recipient Name" fields in "<sheet_name>" against "<sanctions_list>"
	Then any match should be flagged for compliance reporting
		And an immediate alert should be sent to AML regulatory authorities
Examples:
| file_name                              | sheet_name | sanctions_list     |
| bank_export_watchlist_screening.csv  | N/A        | FATF High-Risk List |
| bank_export_blacklisted_entities.xlsx | Sheet1     | OFAC SDN List      |
---
@aml_compliance @edge_case @large_files @performance
Scenario Outline: Validate AML compliance checks on large datasets
	Given a bank export file "<file_name>" with over "<row_count>" records
	When I check for AML compliance anomalies
	Then flagged transactions should be identified within "<expected_runtime>"
		And system performance should be optimized for large-scale fraud detection
Examples:
| file_name                               | row_count  | expected_runtime |
| bank_export_large_dataset_aml.csv      | 500,000    | 15 minutes       |
| bank_export_large_dataset_aml.xlsx     | 1,000,000  | 30 minutes       |
