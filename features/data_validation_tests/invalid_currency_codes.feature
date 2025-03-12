@data_validation @currency @export_comparison



Feature: Detect invalid or non-standard currency codes






@invalid_currency_check



Scenario: Ensure all currency codes are valid ISO 4217 codes





	Given I have a bank export file "bank_export_baseline_test.xlsx" from the old system





		And I have a bank export file "bank_export_baseline_test.csv" from the new system





	When I check the currency column





	Then all currency codes should match the ISO 4217 standard





