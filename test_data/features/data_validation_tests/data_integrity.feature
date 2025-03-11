Feature: Validate Data Integrity

  Scenario: Ensure no mandatory fields are empty
    Given a bank export file "transactions.csv"
    When I check the data
    Then no mandatory fields should be empty

  Scenario: Ensure numeric values are valid
    Given a bank export file "transactions.csv"
    When I check the "Amount" column
    Then it should contain only numeric values
