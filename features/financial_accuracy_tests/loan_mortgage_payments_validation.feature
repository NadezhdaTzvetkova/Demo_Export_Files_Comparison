Feature: Loan and Mortgage Payments Validation

  @financial_accuracy @loan_payments @data_integrity
  Scenario Outline: Validate mortgage payment calculations
    Given a bank export file "<file_name>"
    When I compare "Loan Principal", "Interest Rate", and "Monthly Payment" in the "<sheet_name>" sheet
    Then the monthly payment should be calculated using "<loan_formula>"
      And rounding errors should not exceed "<rounding_tolerance>"
      And incorrect calculations should be flagged

    Examples:
      | file_name                           | sheet_name | loan_formula                              | rounding_tolerance |
      | mortgage_export_baseline_test.csv   | N/A        | P*(r(1+r)^n)/((1+r)^n-1)                  | 0.01               |
      | mortgage_export_baseline_test.xlsx  | Sheet1     | P*(r(1+r)^n)/((1+r)^n-1)                  | 0.01               |

  @financial_accuracy @loan_amortization @edge_case
  Scenario Outline: Verify loan amortization schedule consistency
    Given a bank export file "<file_name>"
    When I check the "Amortization Schedule" column in the "<sheet_name>" sheet
    Then all payments should be distributed correctly across the loan term
      And extra payments should be applied to principal correctly
      And any over/underpayment should be flagged for review

    Examples:
      | file_name                              | sheet_name |
      | loan_amortization_schedule_test.csv   | N/A        |
      | loan_amortization_schedule_test.xlsx  | Sheet1     |

  @financial_accuracy @interest_vs_principal @data_analysis
  Scenario Outline: Validate interest vs. principal breakdown in payments
    Given a bank export file "<file_name>"
    When I check "Interest Paid" and "Principal Paid" for each payment in the "<sheet_name>" sheet
    Then the sum of all payments should match the total loan amount plus interest
      And discrepancies should be flagged for further review

    Examples:
      | file_name                                 | sheet_name |
      | mortgage_interest_vs_principal_test.csv  | N/A        |
      | mortgage_interest_vs_principal_test.xlsx | Sheet1     |
