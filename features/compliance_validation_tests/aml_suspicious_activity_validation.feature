Feature: AML Suspicious Activity Validation
    Ensures that bank export transactions comply with AML regulations and detect suspicious activities.

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
