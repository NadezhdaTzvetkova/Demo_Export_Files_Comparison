@regression_tests @historical_data @export_comparison



Feature: Validate consistency of historical data in exports





@historical_data_match



Scenario: Ensure historical transactions remain unchanged across exports




	Given I have a previous bank export file "bank_export_previous_month_test.xlsx"




12 I have a new bank export file "bank_export_baseline_test.xlsx"



	When I compare historical transaction records




	Then historical data should match exactly




