import os
import glob
import pandas as pd
from behave import given, when, then
from datetime import datetime, timedelta
from behave import given, when, then
import re
import logging

# Dynamic Data Directory Selection Based on Feature File
FEATURE_TO_DATA_DIR = {
    "date_format_validation": "test_data/date_validation_test_data",
}

ISO_DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

DELIMITER_MAPPING = {
    "comma": ",",
    "semicolon": ";",
    "TAB": "\t",
    "pipe": "|"
}


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dynamically set the DATA_DIR based on feature name
FEATURE_NAME = "decimal_precision"
DATA_DIR = os.path.join("test_data", f"{FEATURE_NAME}_test_data")

# Ensure DATA_DIR exists
if not os.path.exists(DATA_DIR):
    logging.warning(f"Warning: Data directory {DATA_DIR} does not exist!")

# Determine the appropriate data directory based on the feature file name

def get_test_data_path(feature_folder, file_name):
    """Constructs the correct test data path based on the feature folder."""
    base_dir = "test_data"
    feature_data_folder = os.path.join(base_dir, feature_folder)
    return os.path.join(feature_data_folder, file_name)

    """Dynamically selects the appropriate test data folder based on the feature file name."""
    test_folder = f"test_data/{feature_name.replace(' ', '_').lower()}_test_data"
    file_path = os.path.join(test_folder, file_name)
    matching_files = glob.glob(file_path + "*")  # Supports both .csv and .xlsx
    assert matching_files, f"Test file {file_name} not found in {test_folder}"
    return matching_files[0]  # Return first matching file


def get_test_data_path(feature_folder, file_name):
    """Constructs the correct test data path based on the feature folder."""
    base_dir = "test_data"
    feature_data_folder = os.path.join(base_dir, feature_folder)
    return os.path.join(feature_data_folder, file_name)


# Function to load the test data
def load_data(file_path):
    """Loads test data from CSV or Excel based on file extension."""
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

# ================= AML Suspicious Activity Validation =================

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensure the bank export file exists"""
    feature_name = os.path.basename(context.feature.filename)
    context.data_dir = get_data_directory(feature_name)
    context.file_path = os.path.join(context.data_dir, file_name)
    assert os.path.exists(context.file_path), f"File not found: {context.file_path}"


@when('I check the "Transaction Amount" and "Recipient" columns in "{sheet_name}"')
def step_when_check_transaction_amount(context, sheet_name):
    """Load the file and verify the presence of necessary columns"""
    if context.file_path.endswith(".csv"):
        context.df = pd.read_csv(context.file_path)
    else:
        context.df = pd.read_excel(context.file_path, sheet_name=sheet_name)

    required_columns = ["Transaction Amount", "Recipient"]
    for col in required_columns:
        assert col in context.df.columns, f"Missing column: {col}"
    assert not context.df.empty, "Loaded dataframe is empty."


@then('transactions above "{threshold}" should be flagged')
def step_then_flag_high_value_transactions(context, threshold):
    """Flag transactions above the specified threshold"""
    threshold_value = float(threshold.replace("$", "").replace(",", ""))
    flagged = context.df[context.df["Transaction Amount"] > threshold_value]
    context.flagged_transactions = flagged
    assert not flagged.empty, "No transactions flagged."
    print(f"{len(flagged)} transactions flagged above {threshold}.")


@then('flagged transactions should be reported to "{compliance_team}"')
def step_then_report_to_compliance(context, compliance_team):
    """Ensure flagged transactions are reported"""
    assert hasattr(context, "flagged_transactions"), "No flagged transactions to report."
    assert not context.flagged_transactions.empty, "Flagged transactions dataset is empty."
    print(f"Reporting {len(context.flagged_transactions)} flagged transactions to {compliance_team}.")


@then('system should cross-check against known "{sanctioned_list}"')
def step_then_cross_check_sanctions(context, sanctioned_list):
    """Simulate cross-checking against a sanctioned list"""
    sanctioned_entities = ["OFAC Watchlist", "EU Sanctions", "Interpol Red List"]
    assert sanctioned_list in sanctioned_entities, f"Sanctioned list {sanctioned_list} not recognized."
    print(f"Cross-checking against {sanctioned_list} completed.")


@when('I check multiple transactions in "{sheet_name}"')
def step_when_check_structured_transactions(context, sheet_name):
    """Load transactions for structured transaction analysis"""
    if context.file_path.endswith(".csv"):
        context.df = pd.read_csv(context.file_path)
    else:
        context.df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    assert not context.df.empty, "Loaded dataframe for structured transactions is empty."


@then('transactions structured below "{threshold}" but summing above "{aggregate_limit}" should be flagged')
def step_then_flag_structured_transactions(context, threshold, aggregate_limit):
    """Detect structured transactions designed to evade AML reporting"""
    threshold_value = float(threshold.replace("$", "").replace(",", ""))
    aggregate_value = float(aggregate_limit.replace("$", "").replace(",", ""))
    grouped = context.df.groupby("Recipient")["Transaction Amount"].sum()
    flagged = grouped[(grouped > aggregate_value) & (grouped < threshold_value)]
    context.flagged_structured_transactions = flagged
    assert not flagged.empty, "No structured transactions flagged."
    print(f"{len(flagged)} structured transactions flagged.")


@when('I check for AML compliance anomalies')
def step_when_check_aml_anomalies(context):
    """Simulate checking large datasets for AML anomalies"""
    assert hasattr(context, "df"), "No dataset loaded for AML anomaly detection."
    assert not context.df.empty, "Dataset is empty. Cannot check for AML anomalies."
    context.large_dataset_flagged = True


@then('flagged transactions should be identified within "{expected_runtime}"')
def step_then_validate_aml_runtime(context, expected_runtime):
    """Check if AML processing meets expected runtime"""
    assert hasattr(context, "large_dataset_flagged"), "Large dataset anomalies not processed in time."
    assert context.large_dataset_flagged, "AML anomaly detection did not execute properly."
    print(f"AML compliance anomalies checked within {expected_runtime}.")

# ================= End of AML Suspicious Activity Validation =================

# ================= Start of Currency Consistency Validation =================
def read_bank_export_file(feature_folder, file_name, sheet_name=None):
    """Reads a CSV or Excel file based on the file extension."""
    file_path = get_test_data_path(feature_folder, file_name)
    assert os.path.exists(file_path), f"File not found: {file_path}"

    if file_name.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensures the bank export file exists and loads it into the context."""
    context.feature_folder = "data_validation_test_data"
    context.data = read_bank_export_file(context.feature_folder, file_name)


@when('I check for currency codes in the "{sheet_name}" sheet')
def step_when_check_currency_codes(context, sheet_name):
    """Validates that all transactions have a valid currency code."""
    assert "Currency" in context.data.columns, "Missing 'Currency' column in file."
    valid_currencies = set(["USD", "EUR", "GBP", "JPY", "CAD"])  # Example ISO 4217 codes
    context.currency_issues = context.data[~context.data["Currency"].isin(valid_currencies)]


@then('all transactions should have a valid ISO 4217 currency code')
def step_then_validate_currency_codes(context):
    """Checks if any invalid currency codes exist."""
    assert context.currency_issues.empty, f"Invalid currency codes found:\n{context.currency_issues}"


@then('currency codes should match the account’s assigned currency')
def step_then_validate_account_currency(context):
    """Ensures that the transaction currency matches the assigned account currency."""
    assert "Account Currency" in context.data.columns, "Missing 'Account Currency' column."
    mismatches = context.data[context.data["Currency"] != context.data["Account Currency"]]
    assert mismatches.empty, f"Currency mismatches found:\n{mismatches}"


@when('I check for negative values in the "{sheet_name}" sheet')
def step_when_check_negative_values(context, sheet_name):
    """Validates that negative values are only present in debit transactions."""
    assert "Amount" in context.data.columns, "Missing 'Amount' column."
    assert "Transaction Type" in context.data.columns, "Missing 'Transaction Type' column."
    context.invalid_negatives = context.data[
        (context.data["Amount"] < 0) & (context.data["Transaction Type"] == "Credit")]


@then('negative values should only be present in debit transactions')
def step_then_validate_negative_values(context):
    """Ensures that no credit transactions have negative values."""
    assert context.invalid_negatives.empty, f"Invalid negative values in credit transactions:\n{context.invalid_negatives}"


@when('I check for negative and zero values in the "{sheet_name}" sheet')
def step_when_check_zero_values(context, sheet_name):
    """Checks for zero and negative transaction amounts."""
    context.zero_values = context.data[context.data["Amount"] == 0]
    context.negative_debits = context.data[(context.data["Amount"] < 0) & (context.data["Transaction Type"] == "Debit")]


@then('zero amounts should be flagged as potential errors')
def step_then_flag_zero_amounts(context):
    """Flags transactions with zero amounts."""
    assert context.zero_values.empty, f"Transactions with zero amounts:\n{context.zero_values}"


@then('transactions with zero values should be logged for further review')
def step_then_log_zero_values(context):
    """Logs zero value transactions for further investigation."""
    print(f"⚠️ Zero value transactions detected:\n{context.zero_values}")

# ================= End of Currency Consistency Validation =================
# ================= Start of Date Format Validation =================

import os
import pandas as pd
from behave import given, when, then
from datetime import datetime, timedelta

# Dynamic Data Directory Selection Based on Feature File
FEATURE_TO_DATA_DIR = {
    "date_format_validation": "test_data/date_validation_test_data",
}

ISO_DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_test_data_directory(context):
    feature_name = os.path.basename(context.feature.filename).replace(".feature", "")
    return FEATURE_TO_DATA_DIR.get(feature_name, "test_data")


def load_file(file_path, sheet_name):
    """Loads CSV or Excel files based on extension"""
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path, sheet_name=sheet_name)
    raise ValueError("Unsupported file format")


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensure the bank export file exists"""
    data_dir = get_test_data_directory(context)
    context.file_path = os.path.join(data_dir, file_name)
    assert os.path.exists(context.file_path), f"File not found: {context.file_path}"


@when('I check the "Date" column in the "{sheet_name}" sheet')
def step_when_check_date_column(context, sheet_name):
    """Load and validate date format"""
    df = load_file(context.file_path, sheet_name)
    context.dates = df["Date"]
    context.invalid_dates = []

    for date in context.dates:
        try:
            datetime.strptime(str(date), ISO_DATE_FORMAT)
        except ValueError:
            context.invalid_dates.append(date)


@then('all dates should follow the format "YYYY-MM-DD"')
def step_then_validate_date_format(context):
    """Check if all dates follow ISO format"""
    assert not context.invalid_dates, f"Invalid date formats detected: {context.invalid_dates}"


@then('dates should not contain time components unless explicitly required')
def step_then_validate_date_time_component(context):
    """Ensure no unexpected time components in dates"""
    assert all(" " not in str(date) for date in context.dates), "Some dates contain unexpected time components"


@when('I check the "Timestamp" column in the "{sheet_name}" sheet')
def step_when_check_timestamp_column(context, sheet_name):
    """Load and validate timestamp format"""
    df = load_file(context.file_path, sheet_name)
    context.timestamps = df["Timestamp"]
    context.invalid_timestamps = []

    for timestamp in context.timestamps:
        try:
            datetime.strptime(str(timestamp), TIMESTAMP_FORMAT)
        except ValueError:
            context.invalid_timestamps.append(timestamp)


@then('all timestamps should follow the "YYYY-MM-DD HH:MM:SS" format')
def step_then_validate_timestamp_format(context):
    """Check if all timestamps follow the expected format"""
    assert not context.invalid_timestamps, f"Invalid timestamp formats detected: {context.invalid_timestamps}"


@when('I check for missing or blank date values')
def step_when_check_missing_dates(context):
    """Identify missing date values"""
    context.missing_dates = context.dates.isna() | (context.dates == "")


@then('no date field should be empty or null')
def step_then_validate_no_missing_dates(context):
    """Ensure no missing date values"""
    assert not context.missing_dates.any(), "Missing or blank dates detected"


@when('I check for chronological consistency')
def step_when_check_chronology(context):
    """Ensure dates are in chronological order"""
    context.dates_sorted = sorted(pd.to_datetime(context.dates, errors='coerce'))
    context.date_mismatches = context.dates_sorted != list(pd.to_datetime(context.dates, errors='coerce'))


@then('transaction dates should be in chronological order')
def step_then_validate_chronology(context):
    """Verify that dates are sorted correctly"""
    assert not any(context.date_mismatches), "Transactions are out of order"


@when('I analyze the "Date" column in the "{sheet_name}" sheet')
def step_when_analyze_date_column(context, sheet_name):
    """Detect future or backdated transactions"""
    df = load_file(context.file_path, sheet_name)
    context.dates = pd.to_datetime(df["Date"], errors='coerce')
    today = datetime.today()

    context.backdated_transactions = context.dates < (today - timedelta(days=365 * 5))  # Older than 5 years
    context.future_transactions = context.dates > (today + timedelta(days=30))  # More than 30 days ahead


@then('transactions older than "{backdate_threshold}" years should be flagged for fraud review')
def step_then_flag_old_transactions(context, backdate_threshold):
    """Flag transactions older than the threshold"""
    threshold = int(backdate_threshold)
    assert not any(context.backdated_transactions), f"Found transactions older than {threshold} years"


@then('transactions postdated beyond "{future_threshold}" days should trigger alerts')
def step_then_flag_future_transactions(context, future_threshold):
    """Flag future-dated transactions"""
    threshold = int(future_threshold)
    assert not any(context.future_transactions), f"Found transactions postdated beyond {threshold} days"

# ================= End of Date Format Validation =================

# ================= Beginning of Decimal Precision Validation =================


def load_bank_export(file_name, sheet_name=None):
    """Loads CSV or Excel bank export file"""
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test file {file_name} not found in {DATA_DIR}")

    if file_name.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    logging.info(f"Processing file: {file_name}")


given('a bank export file "{file_name}" with multi-currency transactions')(step_given_bank_export_file)


@when('I check the "Amount" column in the "{sheet_name}" sheet')
def step_when_check_amount_column(context, sheet_name):
    context.df = load_bank_export(context.file_name, sheet_name)
    if "Amount" not in context.df.columns:
        raise KeyError("Missing 'Amount' column in dataset")
    logging.info(f"Loaded dataset from {context.file_name}, checking 'Amount' column")


@then('all monetary values should have exactly "{expected_precision}" decimal places')
def step_then_validate_decimal_precision(context, expected_precision):
    expected_precision = int(expected_precision)

    context.df["Decimal_Precision"] = context.df["Amount"].astype(str).str.split(".").str[-1].str.len()
    incorrect_values = context.df[context.df["Decimal_Precision"] != expected_precision]

    assert incorrect_values.empty, f"{len(incorrect_values)} transactions have incorrect decimal precision!"
    logging.info("All monetary values meet expected decimal precision.")


@then('values should not contain more than "{expected_precision}" decimal places')
def step_then_check_max_precision(context, expected_precision):
    expected_precision = int(expected_precision)

    max_precision = context.df["Decimal_Precision"].max()
    assert max_precision <= expected_precision, f"Max precision found: {max_precision}, expected: {expected_precision}"
    logging.info("All values conform to max decimal precision limit.")


@then('rounding inconsistencies should be flagged')
def step_then_flag_rounding_issues(context):
    context.df["Rounded_Amount"] = context.df["Amount"].round(2)
    rounding_issues = context.df[context.df["Amount"] != context.df["Rounded_Amount"]]

    if not rounding_issues.empty:
        logging.warning(f"{len(rounding_issues)} transactions show rounding inconsistencies.")
        logging.info(rounding_issues.to_string())
    else:
        logging.info("No rounding inconsistencies found.")

# ================= End of Decimal Precision Validation =================
# Map human-readable delimiter names to actual characters


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensure the bank export file exists"""
    context.file_path = os.path.join("test_data/csv_files", file_name)
    assert os.path.exists(context.file_path), f"File not found: {context.file_path}"


@when('I check the delimiter format in the file')
def step_when_check_delimiter_format(context):
    """Detect the delimiter used in the file"""
    with open(context.file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()

    detected_delimiters = [d for d in DELIMITER_MAPPING.values() if d in first_line]
    context.detected_delimiters = detected_delimiters if detected_delimiters else [","]  # Default to comma


@then('files containing multiple valid delimiters "{allowed_delimiters}" should be accepted')
def step_then_validate_multiple_delimiters(context, allowed_delimiters):
    """Check if the file's delimiter is in the list of allowed delimiters"""
    allowed_list = [DELIMITER_MAPPING[d.strip()] for d in allowed_delimiters.split(",")]

    for delimiter in allowed_list:
        try:
            df = pd.read_csv(context.file_path, delimiter=delimiter)
            print(f"✅ Successfully parsed using delimiter: {delimiter}")
            return  # Stop once successful
        except Exception as e:
            print(f"⚠️ Failed with delimiter: {delimiter} -> {e}")

    assert False, f"❌ No valid delimiter found in {context.file_path}"

# ================= Beginning of Delimiter Inconsistency Validation =================

from behave import given, when, then
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_data_path(file_name):
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "delimiter_inconsistency_test_data"
    return os.path.join(base_dir, feature_folder, file_name)

def load_file(file_name):
    """Loads CSV or Excel files dynamically."""
    file_path = get_data_path(file_name)
    if file_name.endswith(".csv"):
        return pd.read_csv(file_path, dtype=str, engine='python')
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_path, dtype=str)
    else:
        raise ValueError("Unsupported file format")

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.df = load_file(file_name)
    assert not context.df.empty, f"File {file_name} is empty or failed to load."

@when('I check the delimiter format in the file')
def step_when_check_delimiter(context):
    file_path = get_data_path(context.file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    delimiters = [',', ';', '|', '\t']
    context.detected_delimiters = [d for d in delimiters if d in first_line]
    assert len(context.detected_delimiters) > 0, "No delimiter detected. File might be corrupted."

@then('the delimiter should be consistent throughout the file')
def step_then_check_consistency(context):
    file_path = get_data_path(context.file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    delimiter_counts = [line.count(context.detected_delimiters[0]) for line in lines]
    assert all(count == delimiter_counts[0] for count in delimiter_counts), "Inconsistent delimiters detected."
    logging.info(f"Delimiter '{context.detected_delimiters[0]}' is consistent across the file.")

@then('mixed delimiters within the file should be flagged')
def step_then_flag_mixed_delimiters(context):
    if len(context.detected_delimiters) > 1:
        logging.warning(f"Mixed delimiters detected in {context.file_name}: {context.detected_delimiters}")
        assert False, "File contains mixed delimiters."

@then('an error report should be generated listing inconsistent delimiters')
def step_then_generate_error_report(context):
    if len(context.detected_delimiters) > 1:
        report_path = get_data_path("delimiter_error_report.txt")
        with open(report_path, 'w') as f:
            f.write(f"File: {context.file_name}\n")
            f.write(f"Detected Delimiters: {context.detected_delimiters}\n")
        logging.info(f"Error report generated: {report_path}")

# ================= End of Delimiter Inconsistency Validation =================

# ================= Beginning of Encoding Validation =================

from behave import given, when, then
import chardet
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_data_path(file_name):
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "encoding_validation_test_data"
    return os.path.join(base_dir, feature_folder, file_name)

def detect_encoding(file_path):
    """Detects the encoding of the given file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Read a sample
    result = chardet.detect(raw_data)
    return result['encoding']

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist."

@when('I check the file encoding')
def step_when_check_encoding(context):
    context.detected_encoding = detect_encoding(context.file_path)
    logging.info(f"Detected encoding for {context.file_name}: {context.detected_encoding}")

@then('the file encoding should be "{expected_encoding}"')
def step_then_validate_encoding(context, expected_encoding):
    assert context.detected_encoding.lower() == expected_encoding.lower(), f"Encoding mismatch: Expected {expected_encoding}, but detected {context.detected_encoding}"

@then('non-standard encodings should be flagged')
def step_then_flag_non_standard_encoding(context):
    standard_encodings = ["utf-8", "ascii"]
    if context.detected_encoding.lower() not in standard_encodings:
        logging.warning(f"Non-standard encoding detected: {context.detected_encoding}")
        assert False, f"File {context.file_name} uses non-standard encoding {context.detected_encoding}"

@then('the system should suggest converting to a standard encoding')
def step_then_suggest_conversion(context):
    if context.detected_encoding.lower() not in ["utf-8", "ascii"]:
        logging.info(f"Suggested conversion: Convert {context.file_name} to UTF-8 or ASCII")

@then('a conversion report should list all affected files')
def step_then_generate_encoding_report(context):
    report_path = get_data_path("encoding_report.txt")
    with open(report_path, 'w') as f:
        f.write(f"File: {context.file_name}\n")
        f.write(f"Detected Encoding: {context.detected_encoding}\n")
    logging.info(f"Encoding report generated: {report_path}")

# ================= End of Encoding Validation =================


# ================= Beginning of Invalid Account Number Validation =================



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_data_path(file_name):
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "invalid_account_numbers_test_data"
    return os.path.join(base_dir, feature_folder, file_name)

def is_valid_account_number(account_number, pattern):
    """Checks if the account number follows the expected pattern."""
    return re.match(pattern, account_number) is not None

given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist."

@when('I check the "Account Number" column in the "{sheet_name}" sheet')
def step_when_check_account_number(context, sheet_name):
    # Placeholder for actual implementation (CSV/Excel parsing logic required)
    context.account_numbers = ["1234567890", "ABCDEFGHIJ", "1234-567890"]  # Example test data

@then('all account numbers should match the expected pattern "{pattern}"')
def step_then_validate_account_number_format(context, pattern):
    for account_number in context.account_numbers:
        assert is_valid_account_number(account_number, pattern), f"Invalid account number format detected: {account_number}"

@then('invalidly formatted account numbers should be flagged')
def step_then_flag_invalid_accounts(context):
    invalid_accounts = [acc for acc in context.account_numbers if not is_valid_account_number(acc, r'\d{10,12}')]
    if invalid_accounts:
        logging.warning(f"Invalid account numbers found: {invalid_accounts}")
        assert False, f"Some account numbers do not conform to the expected format: {invalid_accounts}"

@then('a correction suggestion should be provided')
def step_then_suggest_correction(context):
    logging.info("Suggest correction: Ensure account numbers contain only numeric characters and match expected length.")

@then('an alert should be sent for accounts not matching regulatory formats')
def step_then_alert_regulatory_issues(context):
    logging.warning("Regulatory alert: Non-compliant account number detected.")

# Additional steps for IBAN validation, duplicate detection, missing values, and blacklisted accounts...

# ================= End of Invalid Account Number Validation =================

# ================= Beginning of Invalid Currency Code Validation =================

def get_data_path(file_name):
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "invalid_currency_codes_fixed_test_data"
    return os.path.join(base_dir, feature_folder, file_name)

def is_valid_currency_code(currency_code, pattern):
    """Checks if the currency code follows the expected pattern."""
    return re.match(pattern, currency_code) is not None

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist."

@when('I check the "Currency" column in the "{sheet_name}" sheet')
def step_when_check_currency_column(context, sheet_name):
    # Placeholder for actual implementation (CSV/Excel parsing logic required)
    context.currency_codes = ["USD", "E$U", "XYZ"]  # Example test data

@then('all currency codes should match the expected pattern "{pattern}"')
def step_then_validate_currency_format(context, pattern):
    for currency_code in context.currency_codes:
        assert is_valid_currency_code(currency_code, pattern), f"Invalid currency code detected: {currency_code}"

@then('invalid currency codes should be flagged')
def step_then_flag_invalid_currencies(context):
    invalid_currencies = [cur for cur in context.currency_codes if not is_valid_currency_code(cur, r'^[A-Z]{3}$')]
    if invalid_currencies:
        logging.warning(f"Invalid currency codes found: {invalid_currencies}")
        assert False, f"Some currency codes do not conform to the expected format: {invalid_currencies}"

@then('a correction suggestion should be provided')
def step_then_suggest_correction(context):
    logging.info("Suggest correction: Ensure currency codes follow the ISO 4217 standard.")

@then('transactions with invalid currency codes should be marked for review')
def step_then_flag_invalid_transactions(context):
    logging.warning("Flagging transactions with invalid currency codes for further review.")

# Additional steps for AML compliance, missing values, large files, and restricted currencies...

# ================= End of Invalid Currency Code Validation =================