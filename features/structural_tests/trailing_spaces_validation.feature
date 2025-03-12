@structural_tests @trailing_spaces @export_comparison

Feature: Detect trailing spaces in text fields

@trailing_spaces_check

Scenario Outline: Ensure "<text_column>" does not contain trailing spaces

	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system

12 I have a bank export file "bank_export_baseline_test.csv" from the new system

	When I check the "<text_column>" column

	Then no values should contain leading or trailing spaces

Examples:

| text_column      |

| transaction_id   |

| account_name     |

| customer_name    |

| merchant_name    |

