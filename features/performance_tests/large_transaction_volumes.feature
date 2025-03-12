@performance_tests @large_transactions @export_comparison



Feature: Assess performance under large transaction volumes




@large_transactions_test



Scenario: Ensure system performance does not degrade with large transaction volumes in "bank_export_baseline_test.xlsx" and "bank_export_baseline_test.csv"



Given I have a bank export file "bank_export_baseline_test.xlsx" with large transactions



12 I have a bank export file "bank_export_baseline_test.csv" with large transactions



When I compare the files



Then the validation should complete within acceptable time limits


