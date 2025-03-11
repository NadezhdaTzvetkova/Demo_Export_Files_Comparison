Feature: Handle Empty Files

  Scenario: Detect empty CSV file
    Given a bank export file "empty_transactions.csv"
    When I check the file format
    Then the system should return an error indicating the file is empty
