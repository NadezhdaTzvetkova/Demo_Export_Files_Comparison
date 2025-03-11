Feature: Detect Duplicate Transactions

  Scenario: Ensure unique transaction IDs
    Given a bank export file "transactions.csv"
    When I check for duplicate transactions
    Then there should be no duplicate "Transaction ID" values