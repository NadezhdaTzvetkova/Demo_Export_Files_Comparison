@edge_cases @outliers @export_comparison

Feature: Identify extreme values in numeric fields

@outlier_detection

Scenario Outline: Detect extreme "<numeric_column>" values

	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system

12 I have a bank export file "bank_export_baseline_test.csv" from the new system

	When I check the "<numeric_column>" column

	Then any extreme outliers should be flagged

Examples:

| numeric_column      |

| transaction_amount  |

| account_balance     |

| overdraft_limit     |

| interest_rate       |

