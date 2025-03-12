Feature: Validate File Format

  Scenario: Ensure CSV file format is correct
    Given a bank export file "transactions.csv"
    When I check the file format
    Then the file extension should be ".csv"
    And the file encoding should be "UTF-8"
    And the delimiter should be ","

  Scenario: Ensure Excel file format is correct
    Given a bank export file "transactions.xlsx"
    When I check the file format
    Then the file extension should be ".xlsx"