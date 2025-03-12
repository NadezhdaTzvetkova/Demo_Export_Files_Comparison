Feature: Validate Date Format Consistency
@date_validation @format_check
Scenario Outline: Ensure all dates follow YYYY-MM-DD format
	Given a bank export file "<file_name>"
	When I check the "Date" column in the "<sheet_name>" sheet
	Then all dates should follow the format "YYYY-MM-DD"
		And dates should not contain time components unless explicitly required
		And invalid date formats should be flagged for correction
Examples:
| file_name                              | sheet_name |
| bank_export_baseline_test.csv         | N/A        |
| bank_export_baseline_test.xlsx        | Sheet1     |
@date_validation @invalid_dates @edge_case
Scenario Outline: Detect incorrect or invalid dates
	Given a bank export file "<file_name>"
	When I check the "Date" column in the "<sheet_name>" sheet
	Then dates such as "30-Feb" or "31-Apr" should be flagged as invalid
		And leap year validations should be performed
		And invalid dates should be logged with suggested corrections
Examples:
| file_name                           | sheet_name |
| bank_export_invalid_dates_test.csv  | N/A        |
| bank_export_invalid_dates_test.xlsx | Sheet1     |
@date_validation @chronology_check
Scenario Outline: Ensure chronological consistency of dates
	Given a bank export file "<file_name>"
	When I check the "Date" column in the "<sheet_name>" sheet
	Then transaction dates should be in chronological order
		And future-dated transactions should be flagged for review
		And date inconsistencies should be logged with references to previous transactions
Examples:
| file_name                             | sheet_name |
| bank_export_date_consistency_test.csv | N/A        |
| bank_export_date_consistency_test.xlsx | Sheet1     |
@date_validation @missing_values
Scenario Outline: Detect missing or blank date values
	Given a bank export file "<file_name>"
	When I check the "Date" column in the "<sheet_name>" sheet
	Then no date field should be empty or null
		And missing dates should be flagged
		And the system should suggest an estimated date based on transaction history
Examples:
| file_name                           | sheet_name |
| bank_export_missing_dates_test.csv  | N/A        |
| bank_export_missing_dates_test.xlsx | Sheet1     |
@date_validation @timestamp_consistency @timezone_check
Scenario Outline: Ensure date-time consistency in timestamped transactions
	Given a bank export file "<file_name>"
	When I check the "Timestamp" column in the "<sheet_name>" sheet
	Then all timestamps should follow the "YYYY-MM-DD HH:MM:SS" format
		And timestamps should be in a consistent timezone
		And transactions spanning multiple timezones should include proper UTC offsets
Examples:
| file_name                                  | sheet_name |
| bank_export_timestamp_test.csv            | N/A        |
| bank_export_timestamp_test.xlsx           | Sheet1     |
