@edge_cases @character_limit @export_comparison

Feature: Validate maximum character limit in text fields

@max_character_check

Scenario Outline: Ensure "<column>" does not exceed the allowed character limit

	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system

12 I have a bank export file "bank_export_baseline_test.csv" from the new system

	When I check the "<column>" column

	Then no values should exceed the maximum allowed length

Examples:

| column            |

| customer_name     |

| transaction_id    |

| account_name      |

| transaction_description |

