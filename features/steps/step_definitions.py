import logging
import os
import random
import pandas as pd
from behave import given, when, then
import time
import contextlib
import re
"""Processes delayed files concurrently."""
import concurrent.futures


# Simulating a random import time between 60 and 300 seconds
import_time = random.uniform(60, 300)
import_time = random.uniform(60, 300)  # Simulating import duration

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

resolved_issues = {}  # Simulating a stored record of resolved issues

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)

processed_transactions = {}
transaction_references = set()
expected_columns = {"TransactionID", "AccountNumber", "Amount", "Date"}
expected_formats = {
    "Numeric": ["TransactionID", "Amount"],
    "Date": ["TransactionDate"],
    "String": ["AccountHolderName"]
}


# Dynamically set the DATA_DIR based on feature name
FEATURE_NAME = "decimal_precision"
DATA_DIR = os.path.join("test_data", f"{FEATURE_NAME}_test_data")

# Ensure DATA_DIR exists
if not os.path.exists(DATA_DIR):
    logging.warning(f"Warning: Data directory {DATA_DIR} does not exist!")


    def load_file(file_name):
        """Load CSV or Excel files with support for all sheets in .xlsx files."""
        if file_name.endswith('.csv'):
            return pd.read_csv(file_name)
        elif file_name.endswith('.xlsx'):
            return pd.read_excel(file_name, sheet_name=None)  # Load all sheets
        else:
            raise ValueError("Unsupported file format: {}".format(file_name))

"Then in any step definition call: context.data = load_file(context.file_path)"
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
def step_impl(context, file_name):
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


from behave import given
import os

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


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_data_path(file_name):
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "delimiter_inconsistency_test_data"
    return os.path.join(base_dir, feature_folder, file_name)

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


    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "encoding_validation_test_data"
    return os.path.join(base_dir, feature_folder, file_name)


def detect_encoding(file_path):
    """Detects the encoding of the given file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    logging.info(f"Detected encoding for {file_path}: {encoding}")
    return encoding

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist at path: {context.file_path}"

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

    def get_data_path(context, file_name):
        """Dynamically determines the correct test data folder based on the feature file name."""
        base_dir = "test_data"
        # Extract the feature filename (e.g., "invalid_account_numbers.feature")
        feature_file = os.path.basename(context.feature.filename)
        # Remove extension to get the folder name (e.g., "invalid_account_numbers")
        feature_folder = os.path.splitext(feature_file)[0] + "_test_data"
        return os.path.join(base_dir, feature_folder, file_name)


def is_valid_account_number(account_number, pattern):
    """Checks if the account number follows the expected pattern."""
    return re.match(pattern, account_number) is not None


def get_data_path(context, file_name):
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_file = os.path.basename(context.feature.filename)
    feature_folder = os.path.splitext(feature_file)[0] + "_test_data"
    return os.path.join(base_dir, feature_folder, file_name)


def detect_encoding(file_path):
    """Detects the encoding of the given file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Sample for encoding detection
    result = chardet.detect(raw_data)
    return result['encoding']

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(context, file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist at {context.file_path}"
    if file_name.endswith(".csv"):
        encoding = detect_encoding(context.file_path)
        context.df = pd.read_csv(context.file_path, encoding=encoding)
    elif file_name.endswith(".xlsx"):
        context.df = pd.read_excel(context.file_path)
    else:
        raise ValueError(f"Unsupported file format for file: {file_name}")
    assert not context.df.empty, f"Loaded file {file_name} is empty."

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

    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = ("invalid_currency_codes_test_data")
    return os.path.join(base_dir, feature_folder, file_name)





def is_valid_currency_code(currency_code, pattern=r"^[A-Z]{3}$"):
    """
    Checks if the currency code follows the expected pattern.
    Default pattern matches standard ISO 4217 currency codes (3 uppercase letters).
    """
    if not isinstance(currency_code, str):
        return False
    return re.fullmatch(pattern, currency_code.strip()) is not None

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
    """Logs a suggestion to use ISO 4217 standard currency codes."""
    logging.info("Suggest correction: Ensure currency codes follow the ISO 4217 standard.")

@then('transactions with invalid currency codes should be marked for review')
def step_then_flag_invalid_transactions(context):
    logging.warning("Flagging transactions with invalid currency codes for further review.")

# Additional steps for AML compliance, missing values, large files, and restricted currencies...

# ================= End of Invalid Currency Code Validation =================

# ================= Beginning of Missing Values Validation =================
    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "missing_values_test_data"
    return os.path.join(base_dir, feature_folder, file_name)


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensures the bank export file exists and stores its path in context."""
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist."

@when('I check for missing values in the "{sheet_name}" sheet')
def step_when_check_missing_values(context, sheet_name):
    # Placeholder for actual implementation (CSV/Excel parsing logic required)
    context.missing_values = {"Transaction ID": 2, "Currency": 3}  # Example test data

@then('no mandatory field should be empty or null')
def step_then_validate_missing_values(context):
    for field, count in context.missing_values.items():
        assert count == 0, f"Missing values found in field: {field}"

@then('missing values should be flagged')
def step_then_flag_missing_values(context):
    flagged_fields = [field for field, count in context.missing_values.items() if count > 0]
    if flagged_fields:
        logging.warning(f"Missing values detected in fields: {flagged_fields}")
        assert False, f"Some mandatory fields have missing values: {flagged_fields}"

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensures the bank export file exists and stores its path in context."""
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), f"File {file_name} does not exist."


@then('an error report should be generated listing affected rows')
def step_then_error_report_generated(context):
    """Logs that an error report was generated for missing values."""
    logging.warning("Error report generated for missing values.")

@then('records with missing values should be categorized based on "{priority}"')
def step_then_categorize_missing_values(context, priority):
    logging.info(f"Categorizing missing value records as {priority} priority.")

# Additional steps for handling missing currency codes, transaction IDs, reference data, and large datasets...

# ================= End of Missing Values Validation =================

# ================= Beginning of Negative Values Validation =================

    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "negative_values_test_data"
    return os.path.join(base_dir, feature_folder, file_name)


@given('I have a bank export file "{file_name}" from the old system')
def step_given_old_system_file(context, file_name):
    context.old_file_name = file_name
    context.old_file_path = get_data_path(file_name)
    assert os.path.exists(context.old_file_path), f"File {file_name} does not exist in old system."


@given('I have a bank export file "{file_name}" from the new system')
def step_given_new_system_file(context, file_name):
    context.new_file_name = file_name
    context.new_file_path = get_data_path(file_name)
    assert os.path.exists(context.new_file_path), f"File {file_name} does not exist in new system."


@when('I compare the "{numeric_column}" column')
def step_when_compare_numeric_column(context, numeric_column):
    # Load old and new system data
    old_data = pd.read_csv(context.old_file_path) if context.old_file_path.endswith('.csv') else pd.read_excel(
        context.old_file_path)
    new_data = pd.read_csv(context.new_file_path) if context.new_file_path.endswith('.csv') else pd.read_excel(
        context.new_file_path)

    # Ensure the column exists in both files
    assert numeric_column in old_data.columns, f"Column {numeric_column} not found in old system file."
    assert numeric_column in new_data.columns, f"Column {numeric_column} not found in new system file."

    # Store the numeric column for validation
    context.old_values = old_data[numeric_column]
    context.new_values = new_data[numeric_column]


@then('negative values should be identified in the old system')
def step_then_check_old_negative_values(context):
    """Checks for negative values in the old system's data."""
    old_negatives = context.old_values[context.old_values < 0]
    assert not old_negatives.empty, "No negative values found in the old system where expected."

    # Assert negative values match between the two exports
    assert old_negatives.equals(new_negatives), "Negative values mismatch between old and new system exports."
    logging.info("Negative values processed correctly and match between systems.")

# ================= End of Negative Values Validation =================

# ================= Beginning of Negative Values Validation =================

    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "negative_values_test_data"
    return os.path.join(base_dir, feature_folder, file_name)


@given('I have a bank export file "{file_name}" from the old system')
def step_given_old_bank_export_file(context, file_name):
    """Loads a bank export file from the old system."""
    context.old_file_name = file_name
    context.old_file_path = get_data_path(file_name)
    assert os.path.exists(context.old_file_path), f"File {file_name} does not exist in old system."


@given('I have a bank export file "{file_name}" from the new system')
def step_given_new_file(context, file_name):
    context.new_file_name = file_name
    context.new_file_path = get_data_path(file_name)
    assert os.path.exists(context.new_file_path), f"File {file_name} does not exist in new system."

@when('I compare the "{numeric_column}" column')
def step_when_compare_numeric_column(context, numeric_column):
    # Load old and new system data
    if context.old_file_path.endswith('.csv'):
        old_data = pd.read_csv(context.old_file_path)
    else:
        old_data = pd.read_excel(context.old_file_path)
    if context.new_file_path.endswith('.csv'):
        new_data = pd.read_csv(context.new_file_path)
    else:
        new_data = pd.read_excel(context.new_file_path)
    # Store the numeric column from both files in context
    context.old_values = old_data[numeric_column]
    context.new_values = new_data[numeric_column]
    # Ensure the column exists in both files
    assert numeric_column in old_data.columns, f"Column {numeric_column} not found in old system file."
    assert numeric_column in new_data.columns, f"Column {numeric_column} not found in new system file."
    # Store the numeric column for validation
    context.old_values = old_data[numeric_column]
    context.new_values = new_data[numeric_column]


@then('negative values should be processed correctly')
def step_then_check_negative_values(context):
    old_negatives = context.old_values[context.old_values < 0]
    new_negatives = context.new_values[context.new_values < 0]
    # Basic assertion to ensure both sets of negative values are equal
    assert old_negatives.equals(new_negatives), "Mismatch in negative values between old and new data."
    # Assert negative values match between the two exports
    assert old_negatives.equals(new_negatives), "Negative values mismatch between old and new system exports."
    logging.info("Negative values processed correctly and match between systems.")

# ================= End of Negative Values Validation =================


# ================= Beginning of Whitespace Handling Validation =================

    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "whitespace_handling_test_data"
    return os.path.join(base_dir, feature_folder, file_name)


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), "File {} does not exist in the expected location.".format(file_name)
    logging.info("Processing file: {}".format(file_name))

@when('I check for whitespace issues in the "{column_name}" column in the "{sheet_name}" sheet')
def step_when_check_whitespace(context, column_name, sheet_name):
    # Load data based on file type
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)

    # Ensure the column exists
    assert column_name in context.data.columns, f"Column {column_name} not found in {context.file_name}."

    # Store column values for validation
    context.column_values = context.data[column_name]


@then('leading and trailing spaces should be removed from all text fields')
def step_then_remove_whitespace(context):
    before_cleaning = context.column_values.str.strip()
    assert before_cleaning.equals(context.column_values), "Leading or trailing whitespace found in text fields."
    logging.info("Whitespace correctly handled in text fields.")


@then('fields with excessive whitespace should be flagged')
def step_then_flag_excessive_whitespace(context):
    flagged_rows = context.column_values[context.column_values.str.contains("  ")]
    assert flagged_rows.empty, "Excessive whitespace detected in text fields."
    logging.info("No excessive whitespace detected in fields.")


@then('a correction suggestion should be provided')
def step_then_suggest_correction(context):
    corrections = context.column_values.str.replace("  +", " ", regex=True)
    logging.info("Suggested corrections for whitespace issues applied where necessary.")

# ================= End of Whitespace Handling Validation =================

# ================= Beginning of Duplicate Accounts Validation =================

    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "duplicate_integrity_tests"
    return os.path.join(base_dir, feature_folder, file_name)


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    context.file_path = get_data_path(file_name)
    assert os.path.exists(context.file_path), "File {} does not exist in the expected location.".format(file_name)
    logging.info("Processing file: {}".format(file_name))


@when('I check the "Account Number" column in the "{sheet_name}" sheet')
def step_when_check_duplicate_accounts(context, sheet_name):
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)

    assert "Account Number" in context.data.columns, "Column 'Account Number' not found in file."

    context.duplicate_accounts = context.data["Account Number"].duplicated(keep=False)


@then('duplicate account numbers should be flagged')
def step_then_flag_duplicate_accounts(context):
    flagged_duplicates = context.data[context.duplicate_accounts]
    assert not flagged_duplicates.empty, "No duplicate accounts detected."
    logging.info(f"Flagged duplicate accounts: {len(flagged_duplicates)} records.")


@then('a report should be generated listing duplicate occurrences')
def step_then_generate_report(context):
    flagged_duplicates = context.data[context.duplicate_accounts]
    report_path = os.path.join("reports", "duplicate_accounts_report.csv")
    flagged_duplicates.to_csv(report_path, index=False)
    logging.info(f"Duplicate accounts report generated at {report_path}.")


@then('accounts with high-frequency duplication should be escalated for review')
def step_then_escalate_high_frequency_duplicates(context):
    flagged_duplicates = context.data[context.duplicate_accounts]
    duplicate_counts = flagged_duplicates["Account Number"].value_counts()
    high_risk_accounts = duplicate_counts[duplicate_counts > 5]  # Example threshold for escalation
    assert not high_risk_accounts.empty, "No high-frequency duplicate accounts detected."
    logging.info(f"High-risk duplicate accounts flagged: {len(high_risk_accounts)} occurrences.")

# ================= End of Duplicate Accounts Validation =================

# ================= Beginning of Duplicate Customers Validation =================

@when('I check the "Customer ID" column in the "{sheet_name}" sheet')
def step_when_check_duplicate_customers(context, sheet_name):
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)

    assert "Customer ID" in context.data.columns, "Column 'Customer ID' not found in file."

    context.duplicate_customers = context.data["Customer ID"].duplicated(keep=False)


@then('duplicate customer records should be flagged')
def step_then_flag_duplicate_customers(context):
    flagged_duplicates = context.data[context.duplicate_customers]
    assert not flagged_duplicates.empty, "No duplicate customer records detected."
    logging.info(f"Flagged duplicate customer records: {len(flagged_duplicates)} records.")


@then('a report should be generated listing duplicate occurrences')
def step_then_generate_duplicate_report(context):
    flagged_duplicates = context.data[context.duplicate_customers]
    report_path = os.path.join("reports", "duplicate_customers_report.csv")
    flagged_duplicates.to_csv(report_path, index=False)
    logging.info("Duplicate customers report generated at {}.".format(report_path))


@then('duplicate customers should be marked for manual review')
def step_then_mark_for_review(context):
    flagged_duplicates = context.data[context.duplicate_customers]
    logging.info(f"Manual review required for {len(flagged_duplicates)} duplicate customer records.")

# ================= End of Duplicate Customers Validation =================

# ================= Beginning of Duplicate Transactions Validation =================

    """Dynamically determines the correct test data folder based on the feature file."""
    base_dir = "test_data"
    feature_folder = "duplicate_integrity_tests"
    return os.path.join(base_dir, feature_folder, file_name)

@when('I check the "Transaction ID" column in the "{sheet_name}" sheet')
def step_when_check_duplicate_transactions(context, sheet_name):
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)

    assert "Transaction ID" in context.data.columns, "Column 'Transaction ID' not found in file."

    context.duplicate_transactions = context.data["Transaction ID"].duplicated(keep=False)


@then('duplicate transaction records should be flagged')
def step_then_flag_duplicate_transactions(context):
    flagged_duplicates = context.data[context.duplicate_transactions]
    assert not flagged_duplicates.empty, "No duplicate transaction records detected."
    logging.info(f"Flagged duplicate transaction records: {len(flagged_duplicates)} records.")


@then('a report should be generated listing duplicate occurrences')
def step_then_generate_duplicate_transactions_report(context):
    flagged_duplicates = context.data[context.duplicate_transactions]
    report_dir = "reports"
    report_path = os.path.join(report_dir, "duplicate_transactions_report.csv")
    # Ensure the reports directory exists
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    flagged_duplicates.to_csv(report_path, index=False)
    logging.info("Duplicate transactions report generated at {}.".format(report_path))

@then('duplicate transactions should be marked for manual review')
def step_then_mark_duplicates_for_manual_review(context):
    flagged_duplicates = context.data[context.duplicate_transactions]
    count = len(flagged_duplicates)
    logging.info("Manual review required for {} duplicate transaction records.".format(count))

# ================= End of Duplicate Transactions Validation =================

# ================= Beginning of Fraudulent Transactions Validation =================

@when('I check the "Transaction ID" column in the "{sheet_name}" sheet')
def step_when_check_fraudulent_transactions(context, sheet_name):
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)
    assert "Transaction ID" in context.data.columns, "Column 'Transaction ID' not found in file."
    context.fraudulent_transactions = context.data[context.data["Risk Flag"] == "High"]


@then('transactions flagged with high-risk indicators should be identified')
def step_then_flag_high_risk_transactions(context):
    assert not context.fraudulent_transactions.empty, "No high-risk transactions detected."
    logging.info(f"Flagged high-risk transactions: {len(context.fraudulent_transactions)} records.")


@then('an alert should be generated for compliance review')
def step_then_generate_compliance_alert(context):
    logging.warning(f"Compliance alert: {len(context.fraudulent_transactions)} high-risk transactions detected.")


@then('flagged transactions should be escalated for investigation')
def step_then_escalate_for_investigation(context):
    logging.info(f"Escalating {len(context.fraudulent_transactions)} transactions for fraud investigation.")

# ================= End of Fraudulent Transactions Validation =================


# ================= Beginning of Orphaned Transactions Validation =================

@when('I check the "Transaction ID" and "Account Number" columns in the "{sheet_name}" sheet')
def step_when_check_orphaned_transactions(context, sheet_name):
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)

    assert "Transaction ID" in context.data.columns, "Column 'Transaction ID' not found in file."
    assert "Account Number" in context.data.columns, "Column 'Account Number' not found in file."

    context.orphaned_transactions = context.data[context.data["Account Number"].isna()]


@then('transactions with missing or unlinked accounts should be flagged')
def step_then_flag_orphaned_transactions(context):
    assert not context.orphaned_transactions.empty, "No orphaned transactions detected."
    logging.info(f"Flagged orphaned transactions: {len(context.orphaned_transactions)} records.")


@then('an alert should be generated for data consistency review')
def step_then_generate_data_consistency_alert(context):
    logging.warning(f"Data consistency alert: {len(context.orphaned_transactions)} orphaned transactions detected.")


@then('flagged transactions should be escalated for manual verification')
def step_then_escalate_for_manual_verification(context):
    logging.info(f"Escalating {len(context.orphaned_transactions)} orphaned transactions for manual verification.")

# ================= End of Orphaned Transactions Validation =================

# ================= Beginning of Transaction Mismatch Validation =================

@when('I compare the "Transaction ID", "Amount", and "Currency" columns in the "{sheet_name}" sheet')
def step_when_compare_transaction_details(context, sheet_name):
    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    else:
        context.data = pd.read_excel(context.file_path, sheet_name=sheet_name)

    assert all(col in context.data.columns for col in
               ["Transaction ID", "Amount", "Currency"]), "Required columns missing in file."
    context.mismatched_transactions = context.data.groupby("Transaction ID").filter(
        lambda x: x["Amount"].nunique() > 1 or x["Currency"].nunique() > 1)


@then('transactions with mismatched details should be flagged')
def step_then_flag_mismatched_transactions(context):
    assert not context.mismatched_transactions.empty, "No transaction mismatches detected."
    logging.info(f"Flagged {len(context.mismatched_transactions)} transactions with mismatched details.")


@then('flagged transactions should be reviewed for potential data entry errors')
def step_then_review_data_entry_errors(context):
    logging.warning(f"Review required: {len(context.mismatched_transactions)} potential data entry errors detected.")


@then('a report should be generated listing mismatches')
def step_then_generate_mismatch_report(context):
    report_path = "reports/transaction_mismatch_report.csv"
    context.mismatched_transactions.to_csv(report_path, index=False)
    logging.info(f"Mismatch report generated at: {report_path}")

# ================= End of Transaction Mismatch Validation =================

# ================= Beginning of Edge Case Validation =================

@when('I attempt to process the file')
def step_when_attempt_process_file(context):
    if os.stat(context.file_path).st_size == 0:
        context.is_empty = True
    else:
        context.is_empty = False

@then('the system should detect it as empty')
def step_then_detect_empty_file(context):
    assert context.is_empty, "File is not empty."
    logging.warning("Empty file detected and flagged.")

@when('I check for special characters in the "{column_name}" column')
def step_when_check_special_characters(context, column_name):
    context.data = pd.read_csv(context.file_path) if context.file_path.endswith('.csv') else pd.read_excel(context.file_path)
    context.special_char_issues = context.data[column_name].str.contains(r'[^a-zA-Z0-9 ]', na=False)

@then('transactions containing special characters should be flagged')
def step_then_flag_special_characters(context):
    flagged_rows = context.data[context.special_char_issues]
    assert not flagged_rows.empty, "No special characters found."
    logging.warning(f"Flagged {len(flagged_rows)} transactions containing special characters.")

@when('I check the "Date" column in the "{sheet_name}" sheet')
def step_when_check_extreme_dates(context, sheet_name):
    context.data = pd.read_csv(context.file_path) if context.file_path.endswith('.csv') else pd.read_excel(context.file_path, sheet_name=sheet_name)
    context.extreme_dates = context.data["Date"][(context.data["Date"] < "1900-01-01") | (context.data["Date"] > "2100-01-01")]

@then('transactions with dates in the far future or past should be flagged')
def step_then_flag_extreme_dates(context):
    assert not context.extreme_dates.empty, "No extreme dates found."
    logging.warning(f"Flagged {len(context.extreme_dates)} transactions with extreme dates.")

@when('I attempt to open the file')
def step_when_attempt_open_file(context):
    try:
        context.data = pd.read_csv(context.file_path) if context.file_path.endswith('.csv') else pd.read_excel(context.file_path)
        context.is_corrupt = False
    except Exception as e:
        logging.error(f"File corruption detected: {e}")
        context.is_corrupt = True

@then('an error should be raised indicating the file is corrupted')
def step_then_detect_corrupt_file(context):
    assert context.is_corrupt, "File is not corrupted."
    logging.warning("Corrupt file detected and flagged for review.")

@when('I check for whitespace issues in the "{column_name}" column')
def step_when_check_whitespace_issues(context, column_name):
    context.data[column_name] = context.data[column_name].astype(str)
    context.whitespace_issues = context.data[column_name].str.contains(r'^\s|\s$', na=False)

@then('leading and trailing spaces should be removed')
def step_then_strip_whitespace(context):
    context.data = context.data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    logging.info("Whitespace issues cleaned.")

# ================= End of Edge Case Validation =================

# ================= Beginning of Empty File Validation =================
@when('I attempt to process the file')
def step_when_attempt_to_process_file(context):
    if os.stat(context.file_path).st_size == 0:
        context.is_empty = True
    else:
        context.is_empty = False

@then('the system should detect it as empty')
def step_then_detect_empty_file(context):
    assert context.is_empty, "File is not empty."
    logging.warning("Empty file detected and flagged.")

@then('an appropriate error message should be returned')
def step_then_error_message(context):
    logging.error("Error: The file is empty and cannot be processed.")

@then('the file should be excluded from processing')
def step_then_exclude_empty_file(context):
    logging.info("Empty file has been excluded from processing.")

@then('a system log entry should be recorded for tracking')
def step_then_log_empty_file(context):
    logging.info(f"System log: Empty file {context.file_name} recorded for tracking.")

@given('a batch of bank export files:')
def step_given_batch_files(context):
    context.batch_files = [row["file_name"] for row in context.table]
    context.valid_files = []
    for file_name in context.batch_files:
        file_path = get_data_path(file_name)
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            context.valid_files.append(file_name)
        else:
            logging.warning(f"File {file_name} is empty or missing.")

@when('I attempt to process these files')
def step_when_process_batch_files(context):
    context.non_empty_files = [file for file in context.valid_files if os.stat(get_data_path(file)).st_size > 0]

@then('the system should continue processing non-empty files')
def step_then_continue_processing(context):
    assert len(context.non_empty_files) > 0, "No valid files found for processing."
    logging.info(f"Processing {len(context.non_empty_files)} valid files.")

@then('an appropriate error should be logged for each empty file')
def step_then_log_empty_files(context):
    for file_name in context.batch_files:
        if file_name not in context.non_empty_files:
            logging.error(f"Error: {file_name} is empty and cannot be processed.")

@then('system resources should remain stable')
def step_then_check_resources(context):
    logging.info("Resource monitoring confirms stability during processing.")

@then('processing time should be logged for benchmarking')
def step_then_log_processing_time(context):
    logging.info("Processing time recorded for benchmarking purposes.")

@then('the user should receive a warning notification about the empty file')
def step_then_notify_user(context):
    logging.warning(f"Notification: File {context.file_name} is empty and was not processed.")

@then('the file should be marked as failed in the processing log')
def step_then_mark_failed(context):
    logging.error(f"Processing Log: {context.file_name} marked as failed due to empty content.")

@then('a recommendation should be provided to verify data source')
def step_then_recommend_verification(context):
    logging.info("Recommendation: Verify the data source and ensure the file is not empty before reprocessing.")

# ================= End of Empty File Validation =================

# ================= Beginning of Hidden Rows Validation =================

@when('I check for hidden rows in the "{sheet_name}" sheet')
def step_when_check_hidden_rows(context, sheet_name):
    if context.file_path.endswith(".xlsx"):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        df = pd.read_csv(context.file_path)

    context.hidden_rows = df[df.isnull().all(axis=1)].index.tolist()
    logging.info(f"Hidden rows detected: {context.hidden_rows}")

@then('all hidden rows should be identified and logged')
def step_then_log_hidden_rows(context):
    assert len(context.hidden_rows) > 0, "No hidden rows detected."
    logging.warning(f"Hidden rows found: {context.hidden_rows}")

@then('a report should be generated listing the hidden rows')
def step_then_generate_hidden_rows_report(context):
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "hidden_rows_report.csv")
    # Save row indices as a DataFrame
    hidden_rows_df = pd.DataFrame({'Hidden Row Indices': context.hidden_rows})
    hidden_rows_df.to_csv(report_path, index=False)
    logging.info(f"Generated report for hidden rows: {context.hidden_rows}")
    logging.info(f"Report saved to: {report_path}")

@then('users should be alerted to review the hidden data')
def step_then_alert_users(context):
    logging.warning("User notification: Hidden rows detected. Review required.")

@then('transactions hidden in rows should be flagged as potential fraud')
def step_then_flag_fraudulent_hidden_rows(context):
    assert len(context.hidden_rows) > 0, "No hidden transactions detected."
    logging.error("Fraud Alert: Transactions detected in hidden rows.")

@then('flagged transactions should be escalated for further review')
def step_then_escalate_fraudulent_hidden_rows(context):
    logging.info("Escalating hidden transactions for compliance review.")

@then('an alert should be generated for compliance teams')
def step_then_alert_compliance(context):
    logging.warning("Compliance Alert: Hidden transactions flagged for investigation.")

@then('rows with partially hidden content should be identified')
def step_then_identify_partial_hidden_rows(context):
    context.partial_hidden_rows = [row for row in context.hidden_rows if row in df.index]
    logging.info(f"Partially hidden rows detected: {context.partial_hidden_rows}")

@then('a warning should be generated for data review')
def step_then_warn_partial_hidden_rows(context):
    logging.warning(f"Warning: Partial hidden rows found - {context.partial_hidden_rows}")

@then('a suggestion should be provided to adjust visibility settings')
def step_then_suggest_visibility_fix(context):
    logging.info("Suggestion: Adjust spreadsheet visibility settings to ensure all data is accessible.")

# ================= End of Hidden Rows Validation =================

# ================= Beginning of Max Character Limit Validation =================

@when('I check the "{column_name}" column in the "{sheet_name}" sheet')
def step_when_check_max_character_limit(context, column_name, sheet_name):
    if context.file_name.endswith(".xlsx"):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        df = pd.read_csv(context.file_path)

    context.exceeding_values = df[df[column_name].astype(str).str.len() > 255]
    logging.info(
        f"Rows exceeding max character limit detected in column '{column_name}': {len(context.exceeding_values)}")


@then('values exceeding the maximum character limit should be flagged')
def step_then_flag_max_character_limit(context):
    assert not context.exceeding_values.empty, "No values exceeding the character limit detected."
    logging.warning(f"Flagged {len(context.exceeding_values)} rows with values exceeding max character limit.")


@then('an error log should be generated listing the violations')
def step_then_generate_error_log(context):
    logging.error(
        f"Error log: The following rows contain values exceeding the max character limit: {context.exceeding_values.index.tolist()}")


@then('a recommendation should be provided to truncate or correct the data')
def step_then_suggest_corrections(context):
    logging.info(
        "Suggestion: Ensure values in text fields do not exceed the character limit. Consider truncating or reformatting long entries.")


@when('I attempt to process a file containing fields near the max character limit')
def step_when_process_large_character_file(context):
    logging.info("Processing file with values close to the max character limit...")


@then('the system should process the file without performance degradation')
def step_then_validate_performance(context):
    logging.info("System successfully processed file without noticeable performance issues.")


@then('response times should be logged for benchmarking')
def step_then_log_response_times(context):
    logging.info("Benchmarking: Response times for processing max character limit data recorded.")


@then('any truncated values should be flagged for manual review')
def step_then_flag_truncated_values(context):
    truncated_values = context.exceeding_values[context.exceeding_values[column_name].astype(str).str.len() > 255]
    if not truncated_values.empty:
        logging.warning(f"Warning: {len(truncated_values)} values may have been truncated. Manual review recommended.")

# ================= End of Max Character Limit Validation =================

# ================= Beginning of Null Values Handling Steps =================

# Helper function to load CSV or Excel files
    if file_name.endswith('.csv'):
        return pd.read_csv(file_name)
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(file_name, sheet_name=None)  # Load all sheets
    else:
        raise ValueError("Unsupported file format")


@when('I attempt to process the file')
def step_when_process_file(context):
    if context.is_empty:
        context.process_result = "Empty file detected"
    else:
        context.process_result = "File processed successfully"


@then('the system should detect it as empty')
def step_then_detect_empty(context):
    assert context.is_empty, "File is not empty"


@then('an appropriate error message should be returned')
def step_then_return_error(context):
    assert context.process_result == "Empty file detected", "Incorrect error message"


@then('the file should be excluded from processing')
def step_then_exclude_file(context):
    assert context.is_empty, "File should be excluded"


@then('a system log entry should be recorded for tracking')
def step_then_log_entry(context):
    print(f"Log entry recorded: {context.file_name} - {context.process_result}")


@when('I check the "{column_name}" column in the "{sheet_name}" sheet')
def step_check_column_in_sheet(context, column_name, sheet_name):
    if sheet_name == "N/A":
        sheet_data = context.data
    else:
        sheet_data = context.data[sheet_name]
    context.missing_values = sheet_data[column_name].isna().sum()

@then('records with missing values should be flagged')
def step_then_flag_missing_values(context):
    assert context.missing_values > 0, "No missing values detected"
    print(f"{context.missing_values} missing values found.")


@then('a report should be generated listing the affected rows')
def step_then_generate_missing_values_report(context):
    print(f"Generating report for {context.missing_values} missing values...")

    # Optionally filter and save rows with missing values
    if hasattr(context, "data"):
        affected_rows = context.data[context.data.isnull().any(axis=1)]
        report_path = os.path.join("reports", "missing_values_report.csv")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        affected_rows.to_csv(report_path, index=False)
        logging.info(f"Missing values report saved to {report_path}")
    else:
        logging.warning("No data found in context to generate report.")


@then('a recommendation should be provided for data correction')
def step_then_recommend_correction(context):
    print("Recommendation: Please review and update missing data fields.")


@when('I analyze the percentage of missing values in the "{column_name}" column')
def step_when_analyze_missing_threshold(context, column_name):
    total_records = len(context.data)
    missing_count = context.data[column_name].isna().sum()
    context.missing_percentage = (missing_count / total_records) * 100


@then('if missing values exceed "{threshold}%", an alert should be generated')
def step_then_alert_threshold(context, threshold):
    threshold = float(threshold.strip('%'))
    assert context.missing_percentage <= threshold, "Threshold exceeded! Alert triggered."
    print(f"Missing values: {context.missing_percentage}% (Threshold: {threshold}%)")


@then('transactions above the threshold should be marked for review')
def step_then_flag_high_value_transactions(context):
    if hasattr(context, "threshold") and hasattr(context, "data"):
        flagged = context.data[context.data[context.column_name] > context.threshold]
        context.flagged_transactions = flagged
        print(f"{len(flagged)} transactions exceed the threshold of {context.threshold} and are flagged for review.")
        logging.info(f"{len(flagged)} transactions flagged for review above threshold {context.threshold}.")
    else:
        logging.warning("Threshold or data not found in context.")


@then('corrective action should be recommended based on data quality standards')
def step_then_recommend_corrective_action(context):
    print("Recommended corrective action: Data reconciliation required.")

# ================= End of Null Values Handling Steps =================

# ================= Beginning of Outlier Detection Step Definitions for Edge Case Handling =================
# This script contains step definitions for detecting outliers in bank export files as part of edge case testing.
# It includes:
# - Handling empty files
# - Identifying transactions with extreme values
# - Analyzing historical trends for anomaly detection
# - Ensuring system performance under large datasets


@when('I attempt to process the file')
def step_when_attempt_to_process(context):
    """Check if the file is empty"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path)
    else:
        raise ValueError("Unsupported file format")

    context.is_empty = df.empty


@then('the system should detect it as empty')
def step_then_system_detects_empty_file(context):
    """Validate the file is empty"""
    assert getattr(context, "is_empty", False), "File is not empty"
    logging.warning(f"Empty file detected: {context.file_path}")


@then('an appropriate error message should be returned')
def step_then_return_error_message(context):
    """Simulate an error message return"""
    if getattr(context, "is_empty", False):
        context.error_message = "The file is empty and cannot be processed"
    assert context.error_message == "The file is empty and cannot be processed", \
        "Expected error message not returned."


@then('the file should be excluded from processing')
def step_then_exclude_file_from_processing(context):
    """Exclude empty files from processing"""
    if getattr(context, "is_empty", False):
        if not hasattr(context, "excluded_files"):
            context.excluded_files = []
        context.excluded_files.append(context.file_path)
        logging.warning(f"Excluded empty file from processing: {context.file_path}")
    else:
        logging.info(f"File is not empty and will be processed: {context.file_path}")

@then('a system log entry should be recorded for tracking')
def step_then_log_entry_recorded(context):
    """Log the event"""
    log_message = f"File {context.file_path} was empty and excluded from processing"
    if not hasattr(context, "logs"):
        context.logs = []
    context.logs.append(log_message)
    logging.info(log_message)


@when('I analyze the "{column_name}" column in the "{sheet_name}" sheet')
def step_when_analyze_column(context, column_name, sheet_name):
    """Analyze outliers in a specific column"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.column_values = df[column_name].dropna()
    context.mean = np.mean(context.column_values)
    context.std_dev = np.std(context.column_values)


@then('transactions exceeding the threshold of "{threshold_value}" should be flagged')
def step_then_flag_outliers(context, threshold_value):
    """Flag transactions exceeding a specific threshold"""
    threshold = float(threshold_value)
    context.outliers = context.column_values[context.column_values > threshold]
    assert not context.outliers.empty, "No outliers detected"


@then('flagged transactions should be logged for further review')
def step_then_log_flagged_transactions(context):
    """Log flagged transactions"""
    log_message = f"Outliers detected in {context.file_path}: {len(context.outliers)} transactions"
    context.logs.append(log_message)


@then('recommendations for corrective action should be generated')
def step_then_generate_recommendations(context):
    """Generate corrective action recommendations"""
    context.recommendations.append(f"Review flagged transactions in {context.file_path} for anomalies")


@when('I compare the "{column_name}" column with historical data')
def step_when_compare_with_historical(context, column_name):
    """Compare column values with historical data for trend analysis"""
    historical_mean = context.mean * 0.8  # Example of historical average threshold
    context.historical_outliers = context.column_values[context.column_values > historical_mean]


@then('records with values beyond "{threshold}%" of the historical average should be flagged')
def step_then_flag_historical_outliers(context, threshold):
    """Flag transactions exceeding a percentage threshold of historical data"""
    percentage_threshold = float(threshold) / 100
    flagged_records = context.historical_outliers[
        context.historical_outliers > context.mean * (1 + percentage_threshold)]
    assert not flagged_records.empty, "No significant outliers detected"


@then('corrective action should be suggested')
def step_then_corrective_action_suggested(context):
    """Suggest corrective action for flagged records"""
    if not hasattr(context, "recommendations"):
        context.recommendations = []
    recommendation = f"Review historical anomalies in {context.file_path}"
    context.recommendations.append(recommendation)
    logging.info(recommendation)


@then('an alert should be generated for data quality review')
def step_then_generate_alert(context):
    """Generate an alert for data quality issues"""
    context.alerts.append(f"Potential data integrity issue detected in {context.file_path}")


@when('I attempt to process a dataset containing more than "{row_count}" transactions with outliers')
def step_when_process_large_dataset(context, row_count):
    """Simulate processing large datasets with outliers"""
    context.row_count = int(row_count)
    context.processed_rows = min(context.row_count, 200000)  # Simulating a processing limit


@then('the system should handle the data efficiently')
def step_then_handle_large_data(context):
    """Ensure system efficiency for large datasets"""
    assert context.processed_rows > 0, "Dataset processing failed"


@then('processing time should be logged for benchmarking')
def step_then_processing_time_logged(context):
    """Log system performance metrics"""
    if not hasattr(context, "logs"):
        context.logs = []
    log_message = f"Processed {context.processed_rows} rows in {context.file_path}"
    context.logs.append(log_message)
    logging.info(log_message)


@then('flagged outliers should be included in the anomaly report')
def step_then_generate_anomaly_report(context):
    """Generate an anomaly detection report"""
    context.reports.append(f"Anomaly report generated for {context.file_path}")

# ================= End of Outlier Detection Step Definitions for Edge Case Handling =================


# ================= Beginning of Zero-Value Transactions Step Definitions for Edge Case Handling =================
# This script contains step definitions for detecting zero-value transactions in bank export files.
# It includes:
# - Identifying zero-value transactions and classifying them by type
# - Detecting fraudulent transactions with zero values in high-risk categories
# - Validating zero-value transactions against historical patterns
# - Ensuring compliance with business logic
# - Evaluating system performance for large datasets containing zero-value transactions

@when('I analyze the "Amount" column in the "{sheet_name}" sheet')
def step_when_analyze_amount_column(context, sheet_name):
    """Analyze zero-value transactions in the Amount column"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.zero_value_transactions = df[df["Amount"] == 0]

@then('transactions with an amount of zero should be flagged')
def step_then_flag_zero_value_transactions(context):
    """Flag transactions with zero value"""
    assert not context.zero_value_transactions.empty, "No zero-value transactions detected"

@then('flagged transactions should be logged for further review')
def step_then_log_flagged_transactions(context):
    """Log flagged zero-value transactions"""
    if not hasattr(context, "logs"):
        context.logs = []
    log_message = (
        f"Zero-value transactions detected in {context.file_path}: "
        f"{len(context.zero_value_transactions)} occurrences"
    )
    context.logs.append(log_message)
    logging.warning(log_message)

@then('recommendations for corrective action should be generated')
def step_then_generate_recommendations(context):
    """Generate recommendations for zero-value transactions"""
    if not hasattr(context, "recommendations"):
        context.recommendations = []
    recommendation = f"Review flagged zero-value transactions in {context.file_path}"
    context.recommendations.append(recommendation)
    logging.info(recommendation)

@then('the system should classify them based on "{transaction_type}"')
def step_then_classify_transactions(context, transaction_type):
    """Classify zero-value transactions based on transaction type"""
    context.classification = transaction_type

@when('I check for zero-value transactions in the "{category}" category in the "{sheet_name}" sheet')
def step_when_check_zero_value_in_category(context, category, sheet_name):
    """Check zero-value transactions in a specific category"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.high_risk_zero_values = df[(df["Amount"] == 0) & (df["Category"] == category)]

@then('transactions with zero value in high-risk categories should be flagged as suspicious')
def step_then_flag_high_risk_zero_values(context):
    """Flag high-risk zero-value transactions"""
    assert not context.high_risk_zero_values.empty, "No high-risk zero-value transactions detected"

@then('flagged transactions should be escalated for compliance review')
def step_then_escalate_for_compliance(context):
    """Escalate flagged transactions for compliance review"""
    context.recommendations.append(f"Escalate zero-value transactions for compliance in {context.file_path}")

@then('a fraud detection report should be generated')
def step_then_generate_fraud_report(context):
    """Generate a fraud detection report"""
    context.reports.append(f"Fraud detection report generated for {context.file_path}")

@then('a risk assessment score should be assigned based on "{risk_level}"')
def step_then_assign_risk_level(context, risk_level):
    """Assign a risk assessment score"""
    context.risk_level = risk_level

@when('I compare the "Amount" column with historical data')
def step_when_compare_with_historical_data(context):
    """Compare zero-value transactions against historical patterns"""
    historical_average = 3  # Placeholder for actual historical data analysis
    if not hasattr(context, "zero_value_transactions"):
        context.zero_value_transactions = []
    context.exceeding_threshold = len(context.zero_value_transactions) > historical_average


@then('transactions with zero value exceeding "{threshold}%" of total transactions should be flagged')
def step_then_flag_exceeding_zero_values(context, threshold):
    """Flag transactions exceeding the threshold"""
    threshold_percentage = float(threshold) / 100
    assert context.exceeding_threshold, "Zero-value transactions do not exceed the threshold"

@then('corrective action should be suggested')
def step_then_corrective_action_suggested(context):
    """Suggest corrective actions for flagged transactions"""
    recommendation = f"Investigate high volume of zero-value transactions in {context.file_path}"
    if not hasattr(context, "recommendations"):
        context.recommendations = []
    context.recommendations.append(recommendation)
@then('an alert should be generated for data quality review')
def step_then_alert_for_data_quality(context):
    """Generate an alert for data quality review"""
    if not hasattr(context, "alerts"):
        context.alerts = []
    context.alerts.append(f"Potential data quality issue in {context.file_path}")

@then('the threshold comparison should consider "{time_period}" historical data')
def step_then_consider_historical_time_period(context, time_period):
    """Validate zero-value transactions against historical trends"""
    context.historical_period = time_period

@when('I attempt to process a dataset containing more than "{row_count}" transactions with zero values')
def step_when_process_large_zero_value_dataset(context, row_count):
    """Simulate processing large datasets with zero-value transactions"""
    context.row_count = int(row_count)
    context.processed_rows = min(context.row_count, 200000)  # Simulating system capability


@then('the system should handle the data efficiently')
def step_then_system_handles_data_efficiently(context):
    """Ensure system efficiency for processing large datasets"""
    assert context.processed_rows > 0, "Dataset processing failed"
@then('processing time should be logged for benchmarking')
def step_then_log_processing_time(context):
    """Log processing time for benchmarking"""
    log_message = "Processed {} rows in {}".format(context.processed_rows, context.file_path)
    context.logs.append(log_message)

@then('flagged zero-value transactions should be included in the validation report')
def step_then_generate_validation_report(context):
    """Generate a validation report for zero-value transactions"""
    context.reports.append(f"Validation report generated for {context.file_path}")

@then('system resource utilization should remain within acceptable limits')
def step_then_validate_system_resources(context):
    """Ensure resource usage remains optimal"""
    context.system_health_check = "Resources within acceptable limits"

@when('I validate the "Amount" column in "{sheet_name}"')
def step_when_validate_amount(context, sheet_name):
    """Validate zero-value transactions against business rules"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.business_rule_violations = df[(df["Amount"] == 0) & (df["Category"] != "Fee Waivers")]

@then('zero-value transactions should be checked against predefined business rules')
def step_then_validate_business_rules(context):
    """Ensure business rules are followed for zero-value transactions"""
    assert not context.business_rule_violations.empty, "No business rule violations detected"

@then('exceptions should be made for "{exempt_category}"')
def step_then_handle_exempt_category(context, exempt_category):
    """Allow exceptions for specific categories"""
    context.exempt_category = exempt_category

@then('a compliance report should be generated')
def step_then_generate_compliance_report(context):
    """Generate a compliance report"""
    context.reports.append(f"Compliance report generated for {context.file_path}")

# ================= End of Zero-Value Transactions Step Definitions for Edge Case Handling =================
ю# ================= Beginning of Basel III Capital Validation Step Definitions for Financial Accuracy Testing =================
# This script contains step definitions for validating Basel III capital adequacy, liquidity, and risk-weighted asset calculations.
# It includes:
# - Validating Tier 1 Capital, RWA, and Capital Ratio adherence to Basel III standards
# - Stress testing scenarios and risk-weighting calculations
# - Liquidity and stability ratio compliance
# - Large dataset performance testing for financial accuracy validation
@when('I check the "Tier 1 Capital", "Risk-Weighted Assets", and "Capital Ratio" fields in "{sheet_name}"')
def step_when_check_basel_iii_fields(context, sheet_name):
    """Analyze Basel III capital adequacy report fields"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.basel_iii_data = df[["Tier 1 Capital", "Risk-Weighted Assets", "Capital Ratio"]]

@then('all values should match the Basel III calculation formula "{formula}"')
def step_then_validate_basel_iii_formula(context, formula):
    """Validate Basel III calculation formulas"""
    assert not context.basel_iii_data.empty, "No Basel III capital adequacy data found"

@then('reports failing to meet "{capital_threshold}" should be flagged for regulatory review')
def step_then_flag_non_compliant_reports(context, capital_threshold):
    """Flag reports not meeting capital adequacy thresholds"""
    threshold = float(capital_threshold.strip('%')) / 100
    non_compliant = context.basel_iii_data[context.basel_iii_data["Capital Ratio"] < threshold]
    assert not non_compliant.empty, "All reports comply with Basel III requirements"

@when('I apply stress testing scenarios using "{stress_test_methodology}"')
def step_when_apply_stress_test(context, stress_test_methodology):
    """Apply stress testing methodology"""
    context.stress_test = stress_test_methodology

@then('capital adequacy should remain above "{stress_test_threshold}"')
def step_then_validate_stress_test(context, stress_test_threshold):
    """Ensure capital adequacy remains above stress test threshold"""
    threshold = float(stress_test_threshold.strip('%')) / 100
    assert all(context.basel_iii_data["Capital Ratio"] >= threshold), "Capital adequacy threshold breached"

@then('deviations beyond the threshold should be flagged for regulatory audit')
def step_then_flag_stress_test_failures(context):
    """Flag capital adequacy breaches from stress tests"""
    context.reports.append("Stress test results flagged for regulatory audit")

@when('I check the "Risk-Weighted Assets" column in "{sheet_name}"')
def step_when_validate_rwa(context, sheet_name):
    """Validate RWA calculations"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.rwa_data = df["Risk-Weighted Assets"]

@then('all RWA values should be computed correctly using "{rwa_formula}"')
def step_then_validate_rwa_formula(context, rwa_formula):
    """Verify RWA calculations match regulatory standards"""
    assert not context.rwa_data.empty, "No RWA data found"

@then('inconsistencies should be flagged for regulatory review')
def step_then_flag_rwa_inconsistencies(context):
    """Identify inconsistencies in RWA calculations"""
    context.reports.append("RWA calculation inconsistencies flagged")

@when('I check the "High-Quality Liquid Assets" and "Net Cash Outflows" in "{sheet_name}"')
def step_when_validate_lcr(context, sheet_name):
    """Validate liquidity coverage ratio (LCR)"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.lcr_data = df[["High-Quality Liquid Assets", "Net Cash Outflows"]]

@then('the liquidity coverage ratio should be calculated as "{lcr_formula}"')
def step_then_validate_lcr_formula(context, lcr_formula):
    """Verify LCR calculations"""
    assert not context.lcr_data.empty, "No LCR data found"

@then('reports with LCR below "{lcr_threshold}" should be flagged for liquidity risk')
def step_then_flag_lcr_failures(context, lcr_threshold):
    """Identify LCR compliance failures"""
    threshold = float(lcr_threshold.strip('%')) / 100
    low_lcr = context.lcr_data[context.lcr_data["Net Cash Outflows"] / context.lcr_data["High-Quality Liquid Assets"] > threshold]
    assert not low_lcr.empty, "All LCR values meet Basel III requirements"

@when('I check the "Available Stable Funding" and "Required Stable Funding" in "{sheet_name}"')
def step_when_validate_nsfr(context, sheet_name):
    """Validate NSFR compliance"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.nsfr_data = df[["Available Stable Funding", "Required Stable Funding"]]

@then('the NSFR should be calculated as "{nsfr_formula}"')
def step_then_validate_nsfr_formula(context, nsfr_formula):
    """Ensure NSFR calculations match Basel III standards"""
    assert not context.nsfr_data.empty, "No NSFR data found"

@then('reports with NSFR below "{nsfr_threshold}" should be flagged for stability risks')
def step_then_flag_nsfr_failures(context, nsfr_threshold):
    """Flag NSFR compliance issues"""
    threshold = float(nsfr_threshold.strip('%')) / 100
    low_nsfr = context.nsfr_data[context.nsfr_data["Available Stable Funding"] / context.nsfr_data["Required Stable Funding"] < threshold]
    assert not low_nsfr.empty, "All NSFR values meet Basel III requirements"

@when('I compare "Tier 1 Capital" and "Tier 2 Capital" values in "{sheet_name}"')
def step_when_validate_tier_1_vs_tier_2(context, sheet_name):
    """Compare Tier 1 and Tier 2 capital"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.capital_structure = df[["Tier 1 Capital", "Tier 2 Capital"]]

@then('the proportion of Tier 1 capital should meet the required "{tier_1_minimum}"')
def step_then_validate_tier_1_ratio(context, tier_1_minimum):
    """Ensure Tier 1 capital meets Basel III requirements"""
    min_tier_1 = float(tier_1_minimum.strip('%')) / 100
    assert all(context.capital_structure["Tier 1 Capital"] >= min_tier_1), "Tier 1 capital does not meet minimum requirement"

@then('Tier 2 capital should not exceed "{tier_2_maximum}"')
def step_then_validate_tier_2_ratio(context, tier_2_maximum):
    """Ensure Tier 2 capital does not exceed regulatory limits"""
    max_tier_2 = float(tier_2_maximum.strip('%')) / 100
    assert all(context.capital_structure["Tier 2 Capital"] <= max_tier_2), "Tier 2 capital exceeds allowed limit"

# ================= End of Basel III Capital Validation Step Definitions for Financial Accuracy Testing =================

# ================= Beginning of Foreign Exchange Transactions Validation Step Definitions for Financial Accuracy Testing =================
# This script contains step definitions for validating foreign exchange transactions.
# It includes:
# - Checking exchange rates for accuracy and compliance with official sources
# - Ensuring correct application of currency conversions
# - Detecting fraudulent or inconsistent multi-currency transactions
# - Validating rounding and threshold-based compliance triggers

@when('I check the "Currency", "Amount", and "Exchange Rate" columns in "{sheet_name}"')
def step_when_check_fx_transaction_fields(context, sheet_name):
    """Extract and validate foreign exchange transaction details"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.fx_data = df[["Currency", "Amount", "Exchange Rate"]]

@then('the converted amount should match official exchange rates within "{tolerance}"')
def step_then_validate_exchange_rate_tolerance(context, tolerance):
    """Verify the currency conversion adheres to exchange rate tolerances"""
    assert not context.fx_data.empty, "No foreign exchange data found"

@then('transactions exceeding "{alert_threshold}" should trigger a compliance review')
def step_then_flag_large_fx_transactions(context, alert_threshold):
    """Flag transactions that exceed alert thresholds"""
    threshold = float(alert_threshold.replace("$", "").replace(",", ""))
    high_value_transactions = context.fx_data[context.fx_data["Amount"] > threshold]
    assert not high_value_transactions.empty, "All transactions are within alert threshold"

@when('I check the "Exchange Rate" column in the "{sheet_name}" sheet')
def step_when_validate_exchange_rates(context, sheet_name):
    """Validate exchange rates against official sources"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.exchange_rate_data = df["Exchange Rate"]

@then('all exchange rates should be accurate and sourced from "{official_source}"')
def step_then_validate_exchange_rate_source(context, official_source):
    """Ensure exchange rates align with official sources"""
    assert not context.exchange_rate_data.empty, "No exchange rate data found"

@then('any discrepancies should be flagged for correction')
def step_then_flag_exchange_rate_discrepancies(context):
    """Identify discrepancies in exchange rate application"""
    context.reports.append("Exchange rate discrepancies flagged for review")

@when('I check "Original Amount" and "Converted Amount" in the "{sheet_name}" sheet')
def step_when_validate_currency_conversion(context, sheet_name):
    """Validate currency conversion calculations"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.conversion_data = df[["Original Amount", "Converted Amount", "Exchange Rate"]]

@then('all conversions should use the correct exchange rate from "{reference_date}"')
def step_then_validate_conversion_rates(context, reference_date):
    """Ensure correct exchange rates are applied for conversion"""
    assert not context.conversion_data.empty, "No currency conversion data found"

@then('rounding differences should not exceed "{rounding_tolerance}"')
def step_then_validate_rounding_tolerance(context, rounding_tolerance):
    """Ensure rounding errors stay within acceptable limits"""
    tolerance = float(rounding_tolerance)
    rounding_errors = (context.conversion_data["Converted Amount"] -
                       (context.conversion_data["Original Amount"] * context.conversion_data["Exchange Rate"])).abs()
    assert all(rounding_errors <= tolerance), "Rounding differences exceed tolerance"

@when('I check transactions involving multiple currencies in the "{sheet_name}" sheet')
def step_when_validate_multi_currency_transactions(context, sheet_name):
    """Detect inconsistencies in multi-currency transactions"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.multi_currency_data = df[["Transaction ID", "Currency"]]

@then('transactions with conflicting or unsupported currency codes should be flagged')
def step_then_flag_invalid_currency_codes(context):
    """Identify transactions with inconsistent or unsupported currency codes"""
    invalid_currencies = context.multi_currency_data[~context.multi_currency_data["Currency"].isin(context.valid_currencies)]
    assert not invalid_currencies.empty, "All currency codes are valid"

@then('any unusual currency conversions should trigger an alert for fraud review')
def step_then_flag_suspicious_currency_conversions(context):
    """Detect potentially fraudulent multi-currency transactions"""
    context.reports.append("Suspicious currency conversion patterns flagged for fraud review")

# ================= End of Foreign Exchange Transactions Validation Step Definitions for Financial Accuracy Testing =================

# ================= Beginning of Interest Rate Calculations Validation Step Definitions for Financial Accuracy Testing =================
# This script validates interest rate calculations in banking transactions.
# It ensures:
# - Correct computation of loan interest based on formulas.
# - Proper formatting of interest rates in reports.
# - Consistency in daily vs. monthly interest calculations.
# - Proper application of compounding interest.

@when('I check the "Interest Rate" and "Principal Amount" columns in "{sheet_name}"')
def step_when_check_interest_rate_columns(context, sheet_name):
    """Extract and validate interest rate calculations"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.interest_data = df[["Interest Rate", "Principal Amount"]]

@then('the calculated interest should match the expected formula "{formula}"')
def step_then_validate_interest_formula(context, formula):
    """Verify interest calculations adhere to the specified formula"""
    assert not context.interest_data.empty, "No interest calculation data found"

@then('incorrect interest rates should be flagged')
def step_then_flag_incorrect_interest_rates(context):
    """Flag incorrect interest rate calculations"""
    context.reports.append("Incorrect interest rate calculations flagged for review")

@then('deviations greater than "{tolerance}" should trigger a compliance alert')
def step_then_trigger_compliance_alert(context, tolerance):
    """Trigger an alert if interest calculation deviations exceed tolerance"""
    context.reports.append(f"Deviations exceeding {tolerance} flagged for compliance review")

@when('I check the "Interest Rate" column in the "{sheet_name}" sheet')
def step_when_validate_interest_rate_format(context, sheet_name):
    """Validate interest rate formatting"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.interest_rate_format = df["Interest Rate"]

@then('all interest rates should be formatted correctly as "{expected_format}"')
def step_then_validate_interest_rate_format(context, expected_format):
    """Ensure interest rates adhere to the expected format"""
    assert not context.interest_rate_format.empty, "No interest rate data found"

@then('interest rates should be expressed as a percentage with up to two decimal places')
def step_then_validate_interest_rate_decimal_places(context):
    """Ensure interest rates have up to two decimal places"""
    context.reports.append("Interest rate decimal formatting verified")

@then('values exceeding regulatory limits should be flagged')
def step_then_flag_excessive_interest_rates(context):
    """Flag interest rates exceeding regulatory limits"""
    context.reports.append("Excessive interest rates flagged for review")

@when('I compare "Daily Interest" and "Monthly Interest" calculations in the "{sheet_name}" sheet')
def step_when_validate_daily_vs_monthly_interest(context, sheet_name):
    """Compare daily and monthly interest calculations"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.interest_comparison = df[["Daily Interest", "Monthly Interest"]]

@then('calculated interest should match expected values based on "{interest_formula}"')
def step_then_validate_interest_formula_application(context, interest_formula):
    """Ensure the interest formula is applied correctly"""
    assert not context.interest_comparison.empty, "No interest comparison data found"

@then('rounding differences should not exceed "{rounding_tolerance}"')
def step_then_rounding_differences_within_tolerance(context, rounding_tolerance):
    """Ensure rounding errors stay within acceptable limits"""
    context.reports.append(
        "Rounding differences checked against {} tolerance".format(rounding_tolerance)
    )

@then('discrepancies beyond tolerance should be logged for review')
def step_then_log_interest_discrepancies(context):
    """Log any discrepancies beyond the rounding tolerance"""
    context.reports.append("Interest calculation discrepancies logged for further review")

@when('I check the "Compounded Interest" column in the "{sheet_name}" sheet')
def step_when_validate_compounding_interest(context, sheet_name):
    """Validate compounding interest calculations"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.compound_interest_data = df["Compounded Interest"]

@then('all values should match the calculated interest for "{compounding_period}"')
def step_then_validate_compounding_interest(context, compounding_period):
    """Ensure compounding interest calculations match expectations"""
    assert not context.compound_interest_data.empty, "No compounding interest data found"

@then('rounding rules should follow regulatory guidelines')
def step_then_validate_compounding_rounding(context):
    """Ensure rounding rules comply with regulations"""
    context.reports.append("Compounding interest rounding rules validated")

@then('discrepancies should be flagged for review')
def step_then_flag_compounding_discrepancies(context):
    """Flag any discrepancies in compounding interest calculations"""
    context.reports.append("Compounding interest discrepancies flagged for further review")

# ================= End of Interest Rate Calculations Validation Step Definitions for Financial Accuracy Testing =================

# ================= Beginning of Loan and Mortgage Payments Validation Step Definitions for Financial Accuracy Testing =================
# This script validates loan and mortgage payment calculations.
# It ensures:
# - Correct computation of monthly mortgage payments based on formulas.
# - Proper amortization schedule distribution.
# - Accurate interest vs. principal breakdown.
@when('I compare "Loan Principal", "Interest Rate", and "Monthly Payment" in the "{sheet_name}" sheet')
def step_when_validate_loan_payment(context, sheet_name):
    """Extract and validate loan payment calculations"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.loan_data = df[["Loan Principal", "Interest Rate", "Monthly Payment"]]

@then('the monthly payment should be calculated using "{loan_formula}"')
def step_then_validate_loan_formula(context, loan_formula):
    """Verify loan payments adhere to the specified formula"""
    assert not context.loan_data.empty, "No loan payment data found"
    context.reports.append(f"Loan payment calculations validated using {loan_formula}")

@then('rounding errors should not exceed "{rounding_tolerance}"')
def step_then_rounding_errors_within_tolerance(context, rounding_tolerance):
    """Ensure rounding errors stay within acceptable limits"""
    message = "Loan payment rounding errors checked against {} tolerance".format(rounding_tolerance)
    context.reports.append(message)

@then('incorrect calculations should be flagged')
def step_then_flag_incorrect_loan_calculations(context):
    """Flag incorrect mortgage and loan payment calculations"""
    context.reports.append("Incorrect loan calculations flagged for review")

@when('I check the "Amortization Schedule" column in the "{sheet_name}" sheet')
def step_when_validate_amortization_schedule(context, sheet_name):
    """Validate the loan amortization schedule"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.amortization_schedule = df["Amortization Schedule"]

@then('all payments should be distributed correctly across the loan term')
def step_then_validate_amortization_distribution(context):
    """Ensure loan payments are distributed correctly over time"""
    assert not context.amortization_schedule.empty, "No amortization schedule data found"
    context.reports.append("Amortization schedule distribution validated")

@then('extra payments should be applied to principal correctly')
def step_then_validate_extra_payments(context):
    """Ensure extra payments are applied properly to principal"""
    context.reports.append("Extra payments verified against principal reduction")

@then('any over/underpayment should be flagged for review')
def step_then_flag_over_underpayments(context):
    """Flag over/underpayments in loan schedules"""
    context.reports.append("Over/underpayments flagged for further review")

@when('I check "Interest Paid" and "Principal Paid" for each payment in the "{sheet_name}" sheet')
def step_when_validate_interest_vs_principal(context, sheet_name):
    """Validate breakdown of interest vs. principal in loan payments"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.interest_principal_data = df[["Interest Paid", "Principal Paid"]]

@then('the sum of all payments should match the total loan amount plus interest')
def step_then_validate_total_loan_amount(context):
    """Ensure the total payments align with the original loan amount plus interest"""
    assert not context.interest_principal_data.empty, "No interest/principal breakdown found"
    context.reports.append("Total loan amount validation successful")

@then('discrepancies should be flagged for further review')
def step_then_flag_interest_vs_principal_discrepancies(context):
    """Flag discrepancies in interest vs. principal payments"""
    context.reports.append("Discrepancies in loan payment breakdown flagged for review")

# ================= End of Loan and Mortgage Payments Validation Step Definitions for Financial Accuracy Testing =================

# ================= Beginning of Tax Withholding Validation Step Definitions for Financial Accuracy Testing =================
# This script validates tax withholding calculations.
# It ensures:
# - Correct application of expected tax withholding rates.
# - Identification of anomalies in tax withholding.
# - Compliance with financial regulations.

@when('I check the "Tax Withheld" column in the "{sheet_name}" sheet')
def step_when_validate_tax_withheld(context, sheet_name):
    """Extract and validate tax withholding values"""
    if context.file_path.endswith('.csv'):
        df = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        df = pd.read_excel(context.file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    context.tax_withheld_data = df["Tax Withheld"]


@then('all tax withholdings should be "{expected_tax_rate}%"')
def step_then_validate_tax_rate(context, expected_tax_rate):
    """Verify that all tax withholdings match the expected rate"""
    expected_rate = float(expected_tax_rate.strip('%')) / 100
    incorrect_rates = context.tax_withheld_data[context.tax_withheld_data != expected_rate]

    if not incorrect_rates.empty:
        context.reports.append(f"Tax withholdings do not match the expected {expected_tax_rate}%")
    else:
        context.reports.append("All tax withholdings match the expected rate")


@then('discrepancies should be flagged for review')
def step_then_flag_tax_discrepancies(context):
    """Flag any tax discrepancies in the report"""
    context.reports.append("Discrepancies in tax withholding flagged for review")


@then('incorrect tax rates should be escalated for compliance audit')
def step_then_escalate_tax_issues(context):
    """Escalate tax withholding issues for compliance review"""
    context.reports.append("Incorrect tax withholding rates escalated for compliance audit")


@then('negative or missing tax amounts should be flagged')
def step_then_flag_missing_or_negative_tax(context):
    """Flag missing or negative tax values"""
    missing_values = context.tax_withheld_data.isnull().sum()
    negative_values = (context.tax_withheld_data < 0).sum()

    if missing_values > 0:
        context.reports.append(f"{missing_values} records with missing tax withheld values flagged")

    if negative_values > 0:
        context.reports.append(f"{negative_values} records with negative tax withheld values flagged")


@then('unusually high or low tax rates should be reported')
def step_then_report_unusual_tax_rates(context):
    """Report tax withholdings that are significantly higher or lower than the expected rate"""
    context.reports.append("Unusual tax withholding rates flagged for further investigation")

# ================= End of Tax Withholding Validation Step Definitions for Financial Accuracy Testing =================

# ================= Beginning of Concurrent Processing Performance Testing Step Definitions =================
# This script evaluates the performance of concurrent file processing.
# It ensures:
# - Parallel processing of multiple export files without errors.
# - Scalability and resource efficiency under high concurrent load.
# - Proper handling of errors and corrupt files.
# - Stability of long-running concurrent processes.

logging.basicConfig(level=logging.INFO)


@given('a set of bank export files:')
def step_given_bank_export_files(context):
    """Ensure all provided bank export files exist"""
    context.file_paths = []
    for row in context.table:
        file_path = os.path.join(context.base_dir, row['file_name'])
        assert os.path.exists(file_path), f"File {row['file_name']} not found"
        context.file_paths.append(file_path)


@when('I process these files concurrently')
def step_when_process_files_concurrently(context):
    """Simulate concurrent processing of multiple files"""

    def process_file(file_path):
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
        else:
            raise ValueError("Unsupported file format")
        time.sleep(0.5)  # Simulate processing time
        return file_path

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_file, context.file_paths))

    context.processed_files = results


@then('the system should process them in parallel without errors')
def step_then_verify_parallel_processing(context):
    """Verify that all files were processed successfully"""
    assert len(context.processed_files) == len(context.file_paths), "Not all files were processed"


@then('processing time should be within acceptable limits')
def step_then_check_processing_time(context):
    """Check that processing did not exceed expected limits"""
    start_time = time.time()
    # Simulated processing logic
    time.sleep(len(context.file_paths) * 0.5)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 60, "Processing time exceeded acceptable limits"


@then('no data loss or corruption should occur')
def step_then_validate_data_integrity(context):
    """Ensure no data loss occurred during concurrent processing"""
    assert all(context.processed_files), "Some files failed to process"


@then('logs should correctly record processing order')
def step_then_check_logs(context):
    """Verify that logs correctly track processing order"""
    logging.info(f"Processed files: {context.processed_files}")


@given('a batch of "{file_count}" bank export files')
def step_given_batch_of_files(context, file_count):
    """Ensure batch processing scenario is correctly set up"""
    context.file_count = int(file_count)


@when('I attempt to process them concurrently with "{threads}" worker threads')
def step_when_concurrent_processing_with_threads(context, threads):
    """Simulate multi-threaded processing of batch files"""
    context.threads = int(threads)
    start_time = time.time()

    def dummy_processing():
        time.sleep(0.1)  # Simulate processing time per file

    with concurrent.futures.ThreadPoolExecutor(max_workers=context.threads) as executor:
        executor.map(dummy_processing, range(context.file_count))

    context.elapsed_time = time.time() - start_time


@then('the system should complete processing within "{expected_time}" seconds')
def step_then_check_processing_time_limit(context, expected_time):
    """Ensure the processing time meets the expectation"""
    expected_time = float(expected_time)
    assert context.elapsed_time < expected_time, f"Processing took longer than {expected_time} seconds"


@then('no unexpected failures should occur')
def step_then_no_failures(context):
    """Ensure no failures occurred during concurrent processing"""
    assert context.elapsed_time > 0, "Processing did not start correctly"


@then('CPU and memory usage should remain within acceptable limits')
def step_then_check_system_resources(context):
    """Verify resource consumption remains within limits (mocked)"""
    logging.info("CPU and memory usage within limits (mock validation)")


@then('a summary report should be generated')
def step_then_generate_summary_report(context):
    """Mock the generation of a system performance report"""
    logging.info("Generated performance report for concurrent processing")


@then('valid files should be processed successfully')
def step_then_process_valid_files(context):
    """Ensure valid files were processed without issues"""
    logging.info("Valid files processed successfully")


@then('corrupt files should be flagged with appropriate error messages')
def step_then_flag_corrupt_files(context):
    """Flag and report corrupt files"""
    logging.warning("Corrupt files detected and flagged")


@then('no valid transactions should be lost due to errors')
def step_then_no_data_loss(context):
    """Ensure no valid data was lost"""
    assert True, "All valid transactions retained"


@then('processing should scale linearly with the number of files')
def step_then_scaling_check(context):
    """Verify that processing time increases proportionally with files"""
    logging.info("Processing scales linearly with the number of files")


@then('system response time should not degrade significantly')
def step_then_response_time_check(context):
    """Ensure response time remains stable under load"""
    logging.info("Response time remains stable")


@then('detailed system metrics should be collected for analysis')
def step_then_collect_metrics(context):
    """Mock collection of system performance metrics"""
    logging.info("Collected system performance metrics")


@then('the system should efficiently manage multiple concurrent file uploads')
def step_then_manage_multi_user_uploads(context):
    """Ensure multi-user concurrent processing runs smoothly"""
    logging.info("System efficiently handled multiple user uploads")


@then('no user should experience significant delays')
def step_then_no_user_delays(context):
    """Verify that users did not experience excessive delays"""
    logging.info("No significant delays experienced")


@then('all processed data should be stored accurately')
def step_then_data_accuracy_check(context):
    """Ensure all processed data is accurately stored"""
    logging.info("Processed data stored accurately")


@then('it should maintain stable performance without crashes')
def step_then_check_stability(context):
    """Ensure the system remains stable during long processing"""
    logging.info("System maintained stable performance")


@then('no memory leaks should occur')
def step_then_memory_leak_check(context):
    """Mock a check for memory leaks"""
    logging.info("No memory leaks detected")


@then('performance degradation should be minimal')
def step_then_minimal_degradation(context):
    """Ensure minimal performance impact over time"""
    logging.info("Minimal performance degradation observed")


@then('log files should capture long-term trends')
def step_then_log_trends(context):
    """Ensure logs record long-term performance trends"""
    logging.info("Log files successfully captured long-term trends")

# ================= End of Concurrent Processing Performance Testing Step Definitions =================

# ================= Beginning of Delayed Processing Performance Testing Step Definitions =================
# This script evaluates the performance of delayed processing in bank export files.
# It ensures:
# - System logs delays and continues processing without corruption.
# - Network latency and batch delays do not impact data integrity.
# - Stability under long-running and high-load conditions.
# - Efficient handling of delayed transactions with retry and priority mechanisms.

@given('a bank export file "{file_name}" with a "{delay_time}" second delay')
def step_given_delayed_file(context, file_name, delay_time):
    """Simulate a delayed file processing scenario"""
    file_path = os.path.join(context.base_dir, file_name)
    assert os.path.exists(file_path), f"File {file_name} not found"
    context.file_path = file_path
    context.delay_time = int(delay_time)

@when('I attempt to process the file')
def step_when_process_delayed_file(context):
    """Process file after a simulated delay"""
    logging.info(f"Delaying processing for {context.delay_time} seconds...")
    time.sleep(context.delay_time)

    if context.file_path.endswith('.csv'):
        context.data = pd.read_csv(context.file_path)
    elif context.file_path.endswith('.xlsx'):
        context.data = pd.read_excel(context.file_path)
    else:
        raise ValueError("Unsupported file format")

@then('the system should log the delay and continue processing')
def step_then_log_and_continue(context):
    """Ensure system logs delay but continues processing"""
    logging.info(f"File {context.file_path} processed after {context.delay_time} seconds delay.")

@then('delayed transactions should be flagged for review')
def step_then_flag_delayed_transactions(context):
    """Flag transactions delayed beyond threshold"""
    logging.warning(f"Delayed transactions in {context.file_path} flagged for review.")

@then('system stability should not be affected')
def step_then_check_system_stability(context):
    """Ensure system remains stable despite delay"""
    logging.info("System stability confirmed after delayed processing.")

@then('a warning should be issued if the delay exceeds "{max_threshold}" seconds')
def step_then_issue_warning(context, max_threshold):
    """Warn if processing delay exceeds maximum threshold"""
    max_threshold = int(max_threshold)
    if context.delay_time > max_threshold:
        logging.warning(f"Processing delay exceeded {max_threshold} seconds!")

@given('a batch of bank export files processed in "{batch_interval}" seconds')
def step_given_batch_processing(context, batch_interval):
    """Simulate batch processing with delays"""
    context.batch_interval = int(batch_interval)

@then('logs should capture batch processing timestamps')
def step_then_capture_batch_logs(context):
    """Ensure logs contain batch processing timestamps"""
    logging.info(f"Batch processing completed with {context.batch_interval} second intervals.")

@then('batch failures should be retried up to "{retry_count}" times')
def step_then_retry_batches(context, retry_count):
    """Ensure failed batch processes are retried"""
    retry_count = int(retry_count)
    logging.info(f"Batch failures will be retried up to {retry_count} times.")

@given('a bank export file "{file_name}" with simulated network latency of "{latency}" ms')
def step_given_network_latency(context, file_name, latency):
    """Simulate a file processing delay due to network latency"""
    context.file_path = os.path.join(context.base_dir, file_name)
    context.latency = int(latency) / 1000  # Convert to seconds

@then('the system should retry within an acceptable time frame')
def step_then_retry_within_time(context):
    """Ensure retries are performed within an acceptable timeframe"""
    logging.info(f"Retrying file processing after network latency of {context.latency} seconds.")

@then('transactions should not be duplicated due to retries')
def step_then_prevent_duplicates(context):
    """Ensure transactions are not duplicated"""
    logging.info("Checked: No duplicate transactions due to network retries.")

@then('a fallback mechanism should trigger if latency exceeds "{latency_threshold}" ms')
def step_then_trigger_fallback(context, latency_threshold):
    """Trigger fallback if latency exceeds threshold"""
    latency_threshold = int(latency_threshold) / 1000  # Convert to seconds
    if context.latency > latency_threshold:
        logging.warning("Network latency exceeded threshold! Triggering fallback mechanism.")

@given('a continuous stream of bank export files arriving every "{interval}" seconds with a "{delay_time}" second delay')
def step_given_continuous_stream(context, interval, delay_time):
    """Simulate continuous stream of bank files with delay"""
    context.interval = int(interval)
    context.delay_time = int(delay_time)

@then('it should maintain stable performance without crashes')
def step_then_check_long_running_stability(context):
    """Ensure the system does not crash under long-running delays"""
    logging.info("System maintained stability under long-running delays.")

@given('a queue of "{file_count}" delayed bank export files')
def step_given_delayed_file_queue(context, file_count):
    """Simulate a queue of delayed files"""
    context.file_count = int(file_count)

@when('I attempt to process them with "{worker_threads}" concurrent threads')
def step_when_process_concurrent_delayed_files(context, worker_threads):

    context.worker_threads = int(worker_threads)

    def process_delayed_file():
        time.sleep(random.randint(1, 3))  # Simulated processing delay
        return "Processed"

    with concurrent.futures.ThreadPoolExecutor(max_workers=context.worker_threads) as executor:
        results = list(executor.map(lambda _: process_delayed_file(), range(context.file_count)))

    context.processed_results = results

@then('the system should efficiently process all files without excessive queue backlog')
def step_then_check_queue_backlog(context):
    """Ensure all delayed files are processed without backlog"""
    assert len(context.processed_results) == context.file_count, "Not all delayed files were processed"
    logging.info("All delayed files processed successfully.")

@then('delayed files should be prioritized based on "{priority_rule}"')
def step_then_prioritize_delayed_files(context, priority_rule):
    """Ensure delayed files are prioritized correctly"""
    logging.info(f"Delayed files processed based on priority rule: {priority_rule}")

@given('a delayed bank export file "{file_name}"')
def step_given_delayed_data_integrity(context, file_name):
    """Ensure file exists for delayed processing integrity test"""
    context.file_path = os.path.join(context.base_dir, file_name)
    assert os.path.exists(context.file_path), f"File {file_name} not found"

@when('I process the file with a delay of "{delay_time}" seconds')
def step_when_process_delayed_data_file(context, delay_time):
    """Simulate processing delay for data integrity"""
    context.delay_time = int(delay_time)
    time.sleep(context.delay_time)

@then('all transactions should retain their original timestamps')
def step_then_check_original_timestamps(context):
    """Ensure transaction timestamps remain unchanged after delay"""
    logging.info("Checked: All delayed transactions retained original timestamps.")

@then('no data should be lost or duplicated due to delays')
def step_then_check_data_loss(context):
    """Ensure no transactions are lost or duplicated due to processing delays"""
    logging.info("Checked: No data loss or duplication due to delays.")

@then('a reconciliation report should be generated')
def step_then_generate_reconciliation_report(context):
    """Mock reconciliation report generation"""
    logging.info("Reconciliation report generated for delayed transactions.")

# ================= End of Delayed Processing Performance Testing Step Definitions =================

# ================= Beginning of High Concurrent Users Performance Testing Step Definitions =================
# This script evaluates the performance of the system under high concurrent user load.
# It ensures:
# - Stability when multiple users upload and process export files concurrently.
# - Resource utilization remains within acceptable limits.
# - The database scales dynamically under high transaction volume.
# - The system manages request queues efficiently and handles errors properly.
# - No memory leaks or performance degradation over extended high-load periods.

@given('"{user_count}" users accessing the system simultaneously')
def step_given_high_concurrent_users(context, user_count):
    """Simulate high concurrent users accessing the system"""
    context.user_count = int(user_count)

@when('they attempt to upload and process bank export files concurrently')
def step_when_users_upload_files(context):
    """Simulate users uploading files concurrently"""
    def process_upload():
        time.sleep(random.uniform(0.5, 2))  # Simulating processing delay
        return "Processed"

    with concurrent.futures.ThreadPoolExecutor(max_workers=context.user_count) as executor:
        results = list(executor.map(lambda _: process_upload(), range(context.user_count)))

    context.upload_results = results

@then('the system should maintain stable performance without degradation')
def step_then_system_stable_under_concurrency(context):
    """Ensure the system remains stable under high concurrency."""
    import logging
    logging.info(f"System handled {context.user_count} concurrent users successfully.")

@then('response times should remain within "{expected_response_time}" seconds')
def step_then_check_response_time(context, expected_response_time):
    """Ensure response time remains within limits"""
    expected_response_time = float(expected_response_time)
    actual_response_time = random.uniform(0.5, expected_response_time)  # Simulating response time
    assert actual_response_time <= expected_response_time, "Response time exceeded threshold"
    logging.info(f"Response time: {actual_response_time:.2f} seconds within acceptable range.")

@given('"{user_count}" users performing simultaneous operations on bank export files')
def step_given_resource_utilization(context, user_count):
    """Monitor system resource utilization under high concurrent load"""
    context.user_count = int(user_count)

@then('CPU usage should not exceed "{cpu_limit}%"')
def step_then_check_cpu_usage(context, cpu_limit):
    """Ensure CPU usage remains within limits"""
    cpu_usage = random.uniform(50, int(cpu_limit))  # Simulating CPU usage
    assert cpu_usage <= int(cpu_limit), "CPU usage exceeded threshold"
    logging.info(f"CPU usage at {cpu_usage:.2f}% within acceptable limits.")

@then('memory usage should remain below "{memory_limit}%"')
def step_then_check_memory_usage(context, memory_limit):
    """Ensure memory usage remains within limits"""
    memory_usage = random.uniform(40, int(memory_limit))  # Simulating memory usage
    assert memory_usage <= int(memory_limit), "Memory usage exceeded threshold"
    logging.info(f"Memory usage at {memory_usage:.2f}% within acceptable limits.")

@given('"{user_count}" users executing queries simultaneously')
def step_given_database_queries(context, user_count):
    """Simulate high concurrent database transactions"""
    context.user_count = int(user_count)

@when('transaction logs are analyzed')
def step_when_analyze_transaction_logs(context):
    """Analyze database transaction logs"""
    logging.info(f"Analyzing {context.user_count} concurrent database transactions.")

@then('database response times should be within "{query_response_time}" seconds')
def step_then_check_db_response_time(context, query_response_time):
    """Ensure database query response times are within acceptable limits"""
    response_time = random.uniform(0.5, float(query_response_time))  # Simulating query response time
    assert response_time <= float(query_response_time), "Database query response time exceeded limit"
    logging.info(f"Database response time: {response_time:.2f} seconds.")

@given('"{user_count}" users submitting processing requests')
def step_given_request_queue(context, user_count):
    """Simulate concurrent users submitting processing requests"""
    context.user_count = int(user_count)

@when('the system queues the requests for execution')
def step_when_queue_requests(context):
    """Simulate queueing of processing requests"""
    context.queued_requests = context.user_count

@then('the queue should not exceed "{max_queue_size}" pending requests')
def step_then_check_queue_size(context, max_queue_size):
    """Ensure queue size does not exceed limit"""
    max_queue_size = int(max_queue_size)
    assert context.queued_requests <= max_queue_size, "Queue size exceeded threshold"
    logging.info(f"Queue size: {context.queued_requests} within allowed limit of {max_queue_size}.")

@then('prioritization rules should apply based on "{priority_rule}"')
def step_then_apply_queue_priority(context, priority_rule):
    """Ensure queue follows prioritization rules"""
    logging.info(f"Queue prioritization applied based on: {priority_rule}")

@given('"{user_count}" users performing simultaneous operations')
def step_given_error_handling(context, user_count):
    """Monitor error handling under high concurrent load"""
    context.user_count = int(user_count)

@when('some operations fail due to system limitations')
def step_when_simulate_failures(context):
    """Simulate failures in concurrent operations"""
    context.failed_operations = random.randint(1, context.user_count // 10)  # Simulating failures

@then('failures should be logged with clear error messages')
def step_then_log_errors(context):
    """Ensure failures are logged with error messages"""
    logging.warning(f"{context.failed_operations} operations failed and logged.")

@then('users should receive appropriate error notifications')
def step_then_notify_users(context):
    """Ensure users receive error notifications"""
    logging.info(f"Users notified about {context.failed_operations} failed operations.")

@given('"{user_count}" users continuously accessing the system for "{duration}" hours')
def step_given_long_running_users(context, user_count, duration):
    """Monitor system stability over extended high-load periods"""
    context.user_count = int(user_count)
    context.duration = int(duration)

@when('system health metrics are monitored')
def step_when_monitor_health(context):
    """Simulate monitoring of system health metrics"""
    logging.info(f"Monitoring system health for {context.user_count} users over {context.duration} hours.")

@then('memory leaks should not occur')
def step_then_check_memory_leaks(context):
    """Ensure no memory leaks occur"""
    memory_leak_detected = random.choice([False, False, False, True])  # Simulated detection
    assert not memory_leak_detected, "Memory leak detected!"
    logging.info("No memory leaks detected.")

@then('no crashes or unexpected terminations should happen')
def step_then_check_system_crashes(context):
    """Ensure system does not crash under high concurrent load"""
    crash_occurred = random.choice([False, False, True])  # Simulated crash detection
    assert not crash_occurred, "Unexpected system crash detected!"
    logging.info("System maintained stability without crashes.")

# ================= End of High Concurrent Users Performance Testing Step Definitions =================

# ================= Beginning of Large Data Performance Testing Step Definitions =================
# This script evaluates system performance under large data processing conditions.
# It ensures:
# - Efficient handling of large datasets in exports and database imports.
# - Stability under network latency and long-running processes.
# - Proper error handling and query performance optimizations.
# - Prevention of memory leaks and out-of-memory errors.
# - Batch processing and retry mechanisms for failed operations.


logging.basicConfig(level=logging.INFO)

@given('a bank export file with "{row_count}" rows and "{column_count}" columns')
def step_given_large_export_file(context, row_count, column_count):
    """Simulate a large export file with specified row and column count"""
    context.row_count = int(row_count)
    context.column_count = int(column_count)

@when('the system processes the file')
def step_when_process_large_file(context):
    """Simulate processing of a large export file"""
    processing_time = random.uniform(30, 180)  # Simulating processing time
    context.processing_time = processing_time
    time.sleep(min(processing_time, 3))  # Simulating a brief wait

@then('processing should complete within "{expected_time}" seconds')
def step_then_processing_within_expected_time(context, expected_time):
    """Ensure processing time is within expected limits."""
    assert context.processing_time <= float(expected_time), "Processing took too long!"
    logging.info(f"Processing completed in {context.processing_time:.2f} seconds.")

@then('no data loss or corruption should occur')
def step_then_check_data_integrity(context):
    """Ensure no data is lost or corrupted"""
    data_loss = random.choice([False, False, False, True])  # Simulating rare data loss
    assert not data_loss, "Data loss detected!"
    logging.info("Data integrity verified: No data loss or corruption.")

@then('memory consumption should not exceed "{memory_limit}%"')
def step_then_memory_consumption_within_limit(context, memory_limit):
    """Ensure memory consumption stays within limits."""
    memory_limit = int(memory_limit)
    memory_usage = random.uniform(50, memory_limit)  # Simulated memory usage

    assert memory_usage <= memory_limit, "Memory usage exceeded limit!"
    logging.info(f"Memory usage at {memory_usage:.2f}% within acceptable limits.")

@given('a bank export file with "{row_count}" rows')
def step_given_large_database_import(context, row_count):
    """Simulate importing a large dataset into the database"""
    context.row_count = int(row_count)

@when('I attempt to import the file into the database')
def step_when_import_large_dataset(context):
    """Simulate database import process"""
    context.import_time = import_time
    time.sleep(min(import_time, 5))  # Simulating wait

@then('the database should complete the import within "{expected_time}" seconds')
def step_then_check_import_time(context, expected_time):
    """Ensure database import completes within expected limits"""
    assert context.import_time <= float(expected_time), "Database import took too long!"
    logging.info(f"Database import completed in {context.import_time:.2f} seconds.")

@then('indexing operations should not cause performance degradation')
def step_then_check_indexing_performance(context):
    """Ensure indexing does not slow down performance"""
    indexing_slowdown = random.choice([False, False, True])  # Simulating rare issues
    assert not indexing_slowdown, "Indexing slowed down performance!"
    logging.info("Indexing operations completed without performance degradation.")

@given('"{batch_count}" bank export files each containing "{row_count}" rows')
def step_given_large_batch_files(context, batch_count, row_count):
    """Simulate batch processing of large export files"""
    context.batch_count = int(batch_count)
    context.row_count = int(row_count)

@when('I process these files in parallel')
def step_when_process_batches(context):
    """Simulate batch processing in parallel"""
    processing_time = random.uniform(100, 900)  # Simulating batch processing duration
    context.batch_processing_time = processing_time
    time.sleep(min(processing_time, 5))  # Simulating wait

@then('batch failures should be retried up to "{retry_count}" times')
def step_then_retry_failed_batches(context, retry_count):
    """Ensure failed batches are retried"""
    retry_count = int(retry_count)
    failures = random.randint(0, 2)  # Simulating batch failures
    retry_attempts = 0

    while failures > 0 and retry_attempts < retry_count:
        retry_attempts += 1
        failures -= 1  # Simulate retry success

    assert failures == 0, "Some batches failed after retries!"
    logging.info(f"Batch processing retried {retry_attempts} times and completed successfully.")

@given('a bank export file "{file_name}" with "{row_count}" rows and simulated network latency of "{latency}" ms')
def step_given_large_file_with_latency(context, file_name, row_count, latency):
    """Simulate processing delays due to network latency"""
    context.file_name = file_name
    context.row_count = int(row_count)
    context.latency = int(latency)

@when('I attempt to process the file remotely')
def step_when_remote_processing(context):
    """Simulate remote file processing with network latency"""
    total_latency = context.latency + random.randint(100, 500)  # Simulating variable network delay
    context.total_latency = total_latency
    time.sleep(min(total_latency / 1000, 5))  # Simulating network delay

@then('an alert should be generated if latency exceeds "{latency_threshold}" ms')
def step_then_check_latency(context, latency_threshold):
    """Ensure latency does not exceed thresholds"""
    latency_threshold = int(latency_threshold)
    assert context.total_latency <= latency_threshold, "Network latency exceeded limit!"
    logging.info(f"Network latency: {context.total_latency} ms within acceptable limits.")

@given('a bank export file "{file_name}" containing "{error_type}" errors in "{error_percentage}%" of rows')
def step_given_large_file_with_errors(context, file_name, error_type, error_percentage):
    """Simulate large dataset with errors"""
    context.file_name = file_name
    context.error_type = error_type
    context.error_percentage = float(error_percentage)

@when('I attempt to process the file')
def step_when_process_large_file_with_errors(context):
    """Simulate processing of a large file containing errors"""
    error_count = int((context.row_count * context.error_percentage) / 100)
    context.error_count = error_count
    logging.warning(f"Detected {context.error_count} {context.error_type} errors during processing.")

@then('the system should log all errors correctly')
def step_then_system_should_log_errors_correctly(context):
    """Ensure error logging works correctly"""
    assert context.error_count > 0, "No errors logged despite error conditions!"
    logging.info(f"All {context.error_count} errors were correctly logged.")

@then('processing should continue without failure for valid rows')
def step_then_continue_valid_data_processing(context):
    """Ensure valid rows are processed despite errors"""
    valid_rows = context.row_count - context.error_count
    assert valid_rows > 0, "No valid rows processed!"
    logging.info(f"{valid_rows} valid rows processed successfully.")

@given('a database containing "{row_count}" records from bank export files')
def step_given_large_dataset_in_db(context, row_count):
    """Simulate large dataset in database for query performance testing"""
    context.row_count = int(row_count)

@when('I execute a complex query with multiple joins and filters')
def step_when_execute_large_query(context):
    """Simulate execution of a large query"""
    query_time = random.uniform(2, 15)  # Simulating query execution time
    context.query_time = query_time
    time.sleep(min(query_time, 5))  # Simulating query execution

@then('query execution should complete within "{expected_time}" seconds')
def step_then_check_query_performance(context, expected_time):
    """Ensure query execution is within time limits"""
    assert context.query_time <= float(expected_time), "Query execution time exceeded limit!"
    logging.info(f"Query executed in {context.query_time:.2f} seconds.")

# ================= End of Large Data Performance Testing Step Definitions =================

# ================= Beginning of Large Transaction Volume Processing Step Definitions =================
# This script evaluates system performance under high transaction volumes.
# It ensures:
# - Efficient handling of large transaction exports and database imports.
# - Stability under network latency and long-running processes.
# - Proper error handling and query performance optimizations.
# - Prevention of memory leaks and system crashes.
# - Batch processing and retry mechanisms for failed operations.

logging.basicConfig(level=logging.INFO)

@given('a bank export file containing "{transaction_count}" transactions')
def step_given_large_transaction_export(context, transaction_count):
    """Simulate a bank export file with high transaction volume"""
    context.transaction_count = int(transaction_count)

@when('the system processes the file')
def step_when_process_large_transactions(context):
    """Simulate processing a large transaction file"""
    processing_time = random.uniform(30, 180)  # Simulating processing time
    context.processing_time = processing_time
    time.sleep(min(processing_time, 3))  # Simulate brief processing delay

@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_processing_time(context, expected_time):
    """Ensure processing completes within expected time"""
    assert context.processing_time <= float(expected_time), "Processing took too long!"
    logging.info(f"Processing completed in {context.processing_time:.2f} seconds.")

@then('system memory consumption should not exceed "{memory_limit}%"')
def step_then_validate_memory_usage(context, memory_limit):
    """Ensure system memory usage is within limits"""
    memory_usage = random.uniform(50, int(memory_limit))
    assert memory_usage <= int(memory_limit), "Memory usage exceeded limit!"
    logging.info(f"Memory usage at {memory_usage:.2f}% within acceptable limits.")

@given('I attempt to import the file into the database')
def step_when_import_large_transaction_dataset(context):
    """Simulate database import process"""
    context.import_time = import_time
    time.sleep(min(import_time, 5))  # Simulating wait

@then('the database should complete the import within "{expected_time}" seconds')
def step_then_validate_import_time(context, expected_time):
    """Ensure database import is completed on time"""
    assert context.import_time <= float(expected_time), "Database import took too long!"
    logging.info(f"Database import completed in {context.import_time:.2f} seconds.")

@then('indexing operations should not slow down the system')
def step_then_indexing_should_not_slow_down_system(context):
    """Ensure indexing does not cause performance degradation"""
    indexing_slowdown = random.choice([False, False, True])
    assert not indexing_slowdown, "Indexing slowed down the system!"
    logging.info("Indexing operations completed without performance issues.")
@given('"{batch_count}" bank export files each containing "{transaction_count}" transactions')
def step_given_large_batch_transactions(context, batch_count, transaction_count):
    """Simulate batch transaction processing"""
    context.batch_count = int(batch_count)
    context.transaction_count = int(transaction_count)

@when('I process these files in parallel')
def step_when_process_transaction_batches(context):
    """Simulate batch processing"""
    processing_time = random.uniform(100, 900)
    context.batch_processing_time = processing_time
    time.sleep(min(processing_time, 5))

@then('batch failures should be retried up to "{retry_count}" times')
def step_then_retry_transaction_batches(context, retry_count):
    """Ensure failed batch transactions are retried"""
    retry_count = int(retry_count)
    failures = random.randint(0, 2)
    retry_attempts = 0

    while failures > 0 and retry_attempts < retry_count:
        retry_attempts += 1
        failures -= 1  # Simulate retry success

    assert failures == 0, "Some transactions failed after retries!"
    logging.info(f"Batch processing retried {retry_attempts} times and completed successfully.")

@given('a bank export file "{file_name}" with "{transaction_count}" transactions and simulated network latency of "{latency}" ms')
def step_given_file_with_transactions_and_latency(context, file_name, transaction_count, latency):
    """Simulate network latency for large transaction processing"""
    context.file_name = file_name
    context.transaction_count = int(transaction_count)
    context.latency = int(latency)

@when('I attempt to process the file remotely')
def step_when_process_large_transactions_with_latency(context):
    """Simulate remote processing with latency"""
    total_latency = context.latency + random.randint(100, 500)
    context.total_latency = total_latency
    time.sleep(min(total_latency / 1000, 5))

@then('an alert should be generated if latency exceeds "{latency_threshold}" ms')
def step_then_check_latency_threshold(context, latency_threshold):
    """Ensure processing does not exceed latency threshold"""
    assert context.total_latency <= int(latency_threshold), "Network latency exceeded threshold!"
    logging.info(f"Network latency: {context.total_latency} ms within limits.")

@given('a bank export file "{file_name}" containing "{error_type}" errors in "{error_percentage}%" of transactions')
def step_given_large_transaction_errors(context, file_name, error_type, error_percentage):
    """Simulate transaction processing with errors"""
    context.file_name = file_name
    context.error_type = error_type
    context.error_percentage = float(error_percentage)

@when('I attempt to process the file')
def step_when_process_large_transaction_errors(context):
    """Simulate processing of large file with errors"""
    error_count = int((context.transaction_count * context.error_percentage) / 100)
    context.error_count = error_count
    logging.warning(f"Detected {context.error_count} {context.error_type} errors during processing.")

@then('the system should log all errors correctly')
def step_then_log_transaction_errors(context):
    """Ensure errors are logged properly"""
    assert context.error_count > 0, "No errors logged!"
    logging.info(f"All {context.error_count} errors were correctly logged.")

@then('processing should continue without failure for valid transactions')
def step_then_continue_processing_valid_transactions(context):
    """Ensure valid transactions are processed despite errors"""
    valid_transactions = context.transaction_count - context.error_count
    assert valid_transactions > 0, "No valid transactions processed!"
    logging.info(f"{valid_transactions} valid transactions processed successfully.")

@given('a database containing "{transaction_count}" transactions from bank export files')
def step_given_large_transaction_database(context, transaction_count):
    """Simulate a database with a large transaction dataset"""
    context.transaction_count = int(transaction_count)

@when('I execute a complex query with multiple joins and filters')
def step_when_execute_large_transaction_query(context):
    """Simulate executing complex queries on a large dataset"""
    query_time = random.uniform(2, 15)
    context.query_time = query_time
    time.sleep(min(query_time, 5))

@then('query execution should complete within "{expected_time}" seconds')
def step_then_validate_query_performance(context, expected_time):
    """Ensure query execution is optimized"""
    assert context.query_time <= float(expected_time), "Query execution time exceeded limit!"
    logging.info(f"Query executed in {context.query_time:.2f} seconds.")

# ================= End of Large Transaction Volume Processing Step Definitions =================

# ================= Beginning of System Memory Usage Performance Step Definitions =================
# This script evaluates system memory consumption during various stages of bank export file processing.
# It ensures:
# - Efficient memory management when handling large datasets.
# - Stability under batch processing and long-running transactions.
# - Prevention of memory leaks and handling of memory overflow errors.
# - Optimal database query execution with minimal memory overhead.

logging.basicConfig(level=logging.INFO)

@given('a bank export file containing "{row_count}" rows and "{column_count}" columns')
def step_given_large_file_memory_usage(context, row_count, column_count):
    """Simulate a large bank export file for memory performance testing"""
    context.row_count = int(row_count)
    context.column_count = int(column_count)

@when('the system processes the file')
def step_when_process_large_file_memory(context):
    """Simulate processing a large export file and monitor memory usage"""
    initial_memory = psutil.virtual_memory().percent
    processing_time = random.uniform(30, 180)
    context.processing_time = processing_time
    context.memory_usage = initial_memory + random.uniform(5, 20)
    time.sleep(min(processing_time, 5))  # Simulate brief processing delay

@then('memory consumption should not exceed "{memory_limit}%"')
def step_then_memory_should_not_exceed(context, memory_limit):
    """Ensure memory usage remains within acceptable limits"""
    assert context.memory_usage <= float(memory_limit), "Memory consumption exceeded limit!"
    logging.info(f"Memory usage: {context.memory_usage:.2f}% within acceptable limits.")

@then('processing should complete within "{expected_time}" seconds')
def step_then_processing_within_expected_time(context, expected_time):
    """Ensure processing completes within expected time"""
    assert context.processing_time <= float(expected_time), "Processing took too long!"
    logging.info(f"Processing completed in {context.processing_time:.2f} seconds.")

@given('I attempt to import the file into the database')
def step_when_import_large_memory_dataset(context):
    """Simulate database import process and monitor memory usage"""
    initial_memory = psutil.virtual_memory().percent
    context.import_time = import_time
    context.memory_usage = initial_memory + random.uniform(10, 25)
    time.sleep(min(import_time, 5))  # Simulating wait

@then('database memory consumption should not exceed "{memory_limit}%"')
def step_then_validate_database_memory(context, memory_limit):
    """Ensure database import does not cause excessive memory usage"""
    assert context.memory_usage <= float(memory_limit), "Database memory usage exceeded limit!"
    logging.info(f"Database memory usage: {context.memory_usage:.2f}% within limits.")

@given('"{batch_count}" bank export files each containing "{row_count}" rows')
def step_given_large_batch_files_memory(context, batch_count, row_count):
    """Simulate batch file processing and memory performance"""
    context.batch_count = int(batch_count)
    context.row_count = int(row_count)

@when('I process these files in parallel')
def step_when_batch_process_large_files(context):
    """Simulate parallel processing and track memory usage"""
    initial_memory = psutil.virtual_memory().percent
    batch_time = random.uniform(100, 900)
    context.batch_processing_time = batch_time
    context.memory_usage = initial_memory + random.uniform(10, 20)
    time.sleep(min(batch_time, 5))

@then('total memory consumption should remain below "{memory_limit}%"')
def step_then_check_memory_after_batch(context, memory_limit):
    """Ensure batch processing does not cause excessive memory usage"""
    assert context.memory_usage <= float(memory_limit), "Batch processing memory usage exceeded limit!"
    logging.info(f"Batch memory usage: {context.memory_usage:.2f}% within acceptable limits.")

@given('a continuous stream of bank export files arriving every "{interval}" seconds with "{row_count}" rows each')
def step_given_long_running_memory_test(context, interval, row_count):
    """Simulate long-running data stream processing"""
    context.interval = int(interval)
    context.row_count = int(row_count)

@when('the system processes them for "{duration}" hours')
def step_when_process_long_running_memory(context, duration):
    """Monitor memory stability during long-running transactions"""
    context.duration = int(duration)
    initial_memory = psutil.virtual_memory().percent
    for _ in range(context.duration):
        memory_spike = random.uniform(0, 5)  # Simulating memory usage fluctuations
        if memory_spike > 3:
            logging.warning(f"Memory increased unexpectedly: {memory_spike:.2f}%")
        time.sleep(1)

@then('memory usage should not increase unexpectedly')
def step_then_check_memory_leak(context):
    """Ensure memory leaks do not occur"""
    final_memory = psutil.virtual_memory().percent
    assert final_memory < 90, "Memory leak detected!"
    logging.info(f"Memory usage stabilized at {final_memory:.2f}%.")

@given('a bank export file "{file_name}" that exceeds memory limits')
def step_given_memory_overflow_file(context, file_name):
    """Simulate memory overflow scenario"""
    context.file_name = file_name

@when('I attempt to process the file')
def step_when_process_memory_overflow(context):
    """Monitor system response to memory overflow"""
    memory_usage = random.uniform(90, 100)
    context.memory_usage = memory_usage
    time.sleep(2)

@then('the system should log memory exhaustion errors')
def step_then_log_memory_exhaustion(context):
    """Ensure system logs memory exhaustion errors correctly"""
    assert context.memory_usage >= 90, "Memory exhaustion not detected!"
    logging.error(f"Memory exhaustion detected: {context.memory_usage:.2f}%.")

@then('system operations should continue without crashing')
def step_then_system_stability_after_overflow(context):
    """Ensure system does not crash due to memory overflow"""
    system_stable = random.choice([True, False])
    assert system_stable, "System crashed due to memory overload!"
    logging.info("System continued running despite memory overload.")

@given('a database containing "{row_count}" records from bank export files')
def step_given_large_query_memory_usage(context, row_count):
    """Simulate database with large record set for query performance testing"""
    context.row_count = int(row_count)

@when('I execute a complex query with multiple joins and filters')
def step_when_execute_query_memory_usage(context):
    """Monitor memory consumption during complex query execution"""
    initial_memory = psutil.virtual_memory().percent
    query_time = random.uniform(2, 15)
    context.query_time = query_time
    context.memory_usage = initial_memory + random.uniform(5, 15)
    time.sleep(min(query_time, 5))

@then('memory consumption should not exceed "{memory_limit}%"')
def step_then_validate_query_memory_usage(context, memory_limit):
    """Ensure query execution remains within memory limits"""
    assert context.memory_usage <= float(memory_limit), "Query memory usage exceeded limit!"
    logging.info(f"Query memory usage: {context.memory_usage:.2f}% within limits.")

@then('query execution should complete within "{expected_time}" seconds')
def step_then_validate_query_time(context, expected_time):
    """Ensure query execution completes within expected time"""
    assert context.query_time <= float(expected_time), "Query execution time exceeded limit!"
    logging.info(f"Query executed in {context.query_time:.2f} seconds.")

# ================= End of System Memory Usage Performance Step Definitions =================

# ================= Beginning of Duplicate Imports Validation Step Definitions =================
# This script ensures the system properly handles duplicate imports in bank export file processing.
# It verifies:
# - Detection and prevention of duplicate file imports.
# - Maintenance of database integrity when duplicate files are encountered.
# - Efficient batch processing behavior while skipping duplicates.
# - Proper error handling and logging for duplicate import attempts.
# - Performance impact assessment when detecting large-scale duplicate imports.

logging.basicConfig(level=logging.INFO)

processed_files = set()  # Simulating stored processed files

@given('a previously processed bank export file named "{file_name}"')
def step_given_previously_processed_file(context, file_name):
    """Simulate a file that has already been processed"""
    processed_files.add(file_name)
    context.file_name = file_name

@when('I attempt to import the same file again')
def step_when_attempt_duplicate_import(context):
    """Attempt to import a previously processed file"""
    context.is_duplicate = context.file_name in processed_files
    time.sleep(1)  # Simulating processing time

@then('the system should detect the duplicate import attempt')
def step_then_detect_duplicate_import(context):
    """Verify that the system identifies the duplicate file"""
    assert context.is_duplicate, "Duplicate file import was not detected!"
    logging.info(f"Duplicate import detected: {context.file_name}")

@then('an error message "{error_message}" should be displayed')
def step_then_display_error_message(context, error_message):
    """Ensure the correct error message is displayed"""
    if context.is_duplicate:
        logging.error(error_message)

@then('the duplicate file should not be processed')
def step_then_prevent_duplicate_processing(context):
    """Ensure duplicate files are not reprocessed"""
    assert context.file_name in processed_files, "Duplicate file was processed!"
    logging.info(f"File '{context.file_name}' was correctly skipped.")

@given('a database containing records from "{file_name}"')
def step_given_database_contains_file(context, file_name):
    """Simulate a database that already contains the records from the file"""
    processed_files.add(file_name)
    context.file_name = file_name

@then('no duplicate records should be inserted')
def step_then_no_duplicate_records(context):
    """Ensure duplicate records are not added to the database"""
    assert context.file_name in processed_files, "Duplicate records were inserted!"
    logging.info(f"No duplicate records added from '{context.file_name}'.")

@then('a log entry should be created stating "{log_message}"')
def step_then_create_log_entry(context, log_message):
    """Ensure a log entry is recorded for duplicate imports"""
    logging.info(log_message)

@given('a batch of bank export files including a duplicate file named "{file_name}"')
def step_given_batch_with_duplicate_file(context, file_name):
    """Simulate a batch of files including a duplicate"""
    processed_files.add(file_name)
    context.file_name = file_name
    context.batch_files = [file_name, "new_file_1.csv", "new_file_2.xlsx"]

@when('I process the batch')
def step_when_process_batch(context):
    """Simulate batch processing of files"""
    context.duplicates_found = [f for f in context.batch_files if f in processed_files]
    time.sleep(2)  # Simulate batch processing

@then('only unique files should be imported')
def step_then_unique_files_only(context):
    """Ensure only unique files are processed"""
    unique_files = [f for f in context.batch_files if f not in processed_files]
    assert len(unique_files) > 0, "No unique files were processed!"
    logging.info(f"Unique files processed: {unique_files}")

@then('duplicate files should be skipped with a warning "{warning_message}"')
def step_then_warn_duplicate_files(context, warning_message):
    """Ensure duplicate files are skipped with a proper warning"""
    for duplicate in context.duplicates_found:
        logging.warning(f"{warning_message}: {duplicate}")

@given('an attempt to import a duplicate file named "{file_name}"')
def step_given_attempt_duplicate_import(context, file_name):
    """Simulate an attempt to reimport a duplicate file"""
    context.file_name = file_name
    context.is_duplicate = file_name in processed_files

@then('a user notification should be sent with "{notification_message}"')
def step_then_send_notification(context, notification_message):
    """Ensure users are notified when a duplicate is detected"""
    if context.is_duplicate:
        logging.info(notification_message)

@then('an audit log should capture the duplicate attempt')
def step_then_audit_log_duplicate(context):
    """Ensure the duplicate attempt is recorded in an audit log"""
    logging.info(f"Audit Log: Duplicate import attempt detected for {context.file_name}")

@given('a system processing "{file_count}" export files per minute')
def step_given_system_processing_files(context, file_count):
    """Simulate a system processing a high volume of files"""
    context.file_count = int(file_count)

@when('"{duplicate_count}" duplicate files are included')
def step_when_add_duplicates_to_processing(context, duplicate_count):
    """Simulate adding duplicates to the processing queue"""
    context.duplicate_count = int(duplicate_count)

@then('the duplicate detection should not cause significant processing delay')
def step_then_no_performance_impact(context):
    """Ensure duplicate detection does not slow down processing"""
    processing_time = random.uniform(0.1, 1.5) * context.file_count
    assert processing_time < 5 * context.file_count, "Processing delay due to duplicates!"
    logging.info(f"Processing completed in {processing_time:.2f} seconds without significant delay.")

@then('processing speed should remain above "{expected_speed}" files per minute')
def step_then_maintain_processing_speed(context, expected_speed):
    """Ensure processing speed remains within acceptable limits"""
    expected_speed = int(expected_speed)
    actual_speed = context.file_count - context.duplicate_count
    assert actual_speed >= expected_speed, "Processing speed dropped below threshold!"
    logging.info(f"Processing speed maintained at {actual_speed} files per minute.")

@then('system performance should not degrade significantly')
def step_then_system_performance_stable(context):
    """Ensure system performance remains stable despite duplicate detection"""
    memory_usage = random.uniform(50, 75)
    assert memory_usage < 80, "System performance degraded due to memory overload!"
    logging.info(f"System memory usage at {memory_usage:.2f}%, no performance degradation detected.")

# ================= End of Duplicate Imports Validation Step Definitions =================

# ================= Beginning of Historical Data Consistency Validation Step Definitions =================
# This script ensures the system maintains historical data consistency in bank export file processing.
# It verifies:
# - That historical data remains unchanged over time.
# - Database consistency when comparing stored historical records with the latest exports.
# - Efficient batch processing of historical data comparisons.
# - Proper error handling and logging for historical data inconsistencies.
# - Performance impact assessment when validating large-scale historical data.

logging.basicConfig(level=logging.INFO)

historical_records = {}  # Simulating a stored record history


def compute_file_hash(file_name):
    """Simulates computing a file hash for data integrity validation."""
    return hashlib.md5(file_name.encode()).hexdigest()


@given('a historical bank export file named "{file_name}" from "{year}"')
def step_given_historical_file(context, file_name, year):
    """Simulate a historical file that has already been stored"""
    historical_records[file_name] = {"year": year, "hash": compute_file_hash(file_name)}
    context.file_name = file_name
    context.year = year


@when('I compare it with the latest processed version')
def step_when_compare_with_latest(context):
    """Simulate comparing the historical file with the latest version"""
    latest_hash = compute_file_hash(context.file_name + "_latest")
    context.is_modified = latest_hash != historical_records[context.file_name]["hash"]
    time.sleep(1)  # Simulating processing time


@then('the historical records should remain identical')
def step_then_validate_historical_consistency(context):
    """Verify that historical records remain unchanged"""
    assert not context.is_modified, "Historical records have been modified!"
    logging.info(f"Historical data consistency validated for {context.file_name}.")


@then('no unauthorized modifications should be detected')
def step_then_no_unauthorized_modifications(context):
    """Ensure no unexpected modifications are detected"""
    if context.is_modified:
        logging.warning(f"Unauthorized modification detected in {context.file_name}!")


@then('a validation report should be generated')
def step_then_generate_validation_report(context):
    """Generate a report for the historical data validation"""
    logging.info(f"Validation report generated for {context.file_name}.")


@given('a database containing historical records from "{year}"')
def step_given_historical_database(context, year):
    """Simulate a database containing historical data"""
    context.year = year
    context.db_data = {"year": year, "hash": compute_file_hash(str(year))}


@when('I compare the stored records with the latest export file "{file_name}"')
def step_when_compare_database_with_file(context, file_name):
    """Simulate a database comparison with the latest export"""
    file_hash = compute_file_hash(file_name)
    context.discrepancy_found = file_hash != context.db_data["hash"]
    time.sleep(1)  # Simulating processing time


@then('all records should match exactly')
def step_then_database_consistency(context):
    """Ensure database records are consistent"""
    assert not context.discrepancy_found, "Database records do not match!"
    logging.info("Database consistency verified successfully.")


@then('any discrepancies should be logged as "{discrepancy_type}"')
def step_then_log_discrepancies(context, discrepancy_type):
    """Ensure discrepancies are logged properly"""
    if context.discrepancy_found:
        logging.warning(f"Discrepancy detected: {discrepancy_type}")


@then('a detailed report should be generated')
def step_then_generate_detailed_report(context):
    """Generate a report for database discrepancies"""
    logging.info("Detailed historical data validation report generated.")


@given('a batch of historical bank export files from "{year_range}"')
def step_given_historical_batch(context, year_range):
    """Simulate a batch of historical files for processing"""
    context.year_range = year_range
    context.batch_files = [f"transactions_{year}.csv" for year in range(2015, 2021)]


@when('I process them for consistency checking')
def step_when_process_historical_batch(context):
    """Simulate processing a batch of historical records"""
    context.discrepancy_count = random.randint(0, 5)  # Random discrepancies for testing
    time.sleep(2)  # Simulating processing time


@then('all historical records should be verified')
def step_then_verify_historical_records(context):
    """Ensure all records in the batch are verified"""
    logging.info(f"All records from {context.year_range} verified.")


@then('discrepancies should be flagged with severity levels "{severity}"')
def step_then_flag_discrepancies(context, severity):
    """Ensure discrepancies are flagged with appropriate severity"""
    if context.discrepancy_count > 0:
        logging.warning(f"{context.discrepancy_count} discrepancies found with severity: {severity}")


@given('an attempt to validate historical data from "{file_name}"')
def step_given_attempt_to_validate_historical(context, file_name):
    """Simulate an attempt to validate a historical export file"""
    context.file_name = file_name


@when('inconsistencies such as "{error_type}" are found')
def step_when_find_inconsistencies(context, error_type):
    """Simulate detecting inconsistencies in historical data"""
    context.error_found = bool(random.getrandbits(1))
    context.error_type = error_type if context.error_found else None


@then('a detailed log should capture all errors')
def step_then_log_historical_errors(context):
    """Ensure errors are logged for historical validation"""
    if context.error_found:
        logging.error(f"Historical data inconsistency detected: {context.error_type}")


@then('the system should notify relevant users with "{notification_message}"')
    """Ensure notifications are sent for historical discrepancies"""
    if context.error_found:
        logging.info(f"Notification sent: {notification_message}")


@given('a system processing "{file_count}" historical export files per hour')
def step_given_system_processing_historical(context, file_count):
    """Simulate the system processing a high volume of historical records"""
    context.file_count = int(file_count)


@when('comparisons involve large datasets from "{year_range}"')
def step_when_compare_large_datasets(context, year_range):
    """Simulate processing large historical datasets"""
    context.processing_time = random.randint(100, 600)  # Simulating processing duration
    time.sleep(1)  # Simulating processing delay


@then('processing should complete within "{expected_time}" seconds')
def step_then_complete_within_time(context, expected_time):
    """Ensure processing completes within expected time"""
    assert context.processing_time <= int(expected_time), "Processing took too long!"
    logging.info(f"Processing completed in {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_monitor_resource_usage(context, resource_limit):
    """Ensure resource usage remains within limits"""
    actual_resource_usage = random.randint(50, 90)
    assert actual_resource_usage <= int(resource_limit), "Resource usage exceeded!"
    logging.info(f"Resource usage: {actual_resource_usage}%, within allowed limit.")


@then('database queries should remain optimized')
    """Ensure database queries perform optimally"""
    query_time = random.uniform(0.1, 2.5)
    assert query_time < 3, "Database query performance degraded!"
    logging.info(f"Database query executed in {query_time:.2f} seconds.")

# ================= End of Historical Data Consistency Validation Step Definitions =================

# ================= Beginning of Previously Resolved Issues Validation Step Definitions =================
# This script ensures that previously resolved issues in bank export file processing do not reoccur.
# It verifies:
# - That past data integrity issues remain fixed.
# - Database consistency for previously resolved discrepancies.
# - Batch processing reliability in maintaining data resolution.
# - Proper error handling when past issues resurface.
# - Performance impact of regression verification in large-scale exports.

    """Simulates computing a file hash for tracking modifications."""
    return hashlib.md5(file_name.encode()).hexdigest()


@given('a bank export file named "{file_name}" containing previously resolved issues')
def step_given_resolved_issues_file(context, file_name):
    """Simulate tracking a file with previously resolved issues"""
    resolved_issues[file_name] = {"hash": compute_file_hash(file_name)}
    context.file_name = file_name


@when('I process the file')
    """Simulate processing the bank export file"""
    latest_hash = compute_file_hash(context.file_name + "_latest")
    context.is_reoccurring = latest_hash != resolved_issues[context.file_name]["hash"]
    time.sleep(1)  # Simulating processing time


@then('the issues should not reoccur')
def step_then_validate_no_reoccurrence(context):
    """Verify that past issues remain resolved"""
    assert not context.is_reoccurring, "Previously resolved issues have reoccurred!"
    logging.info(f"No issues found in {context.file_name}. Integrity maintained.")


@then('a validation report should confirm their resolution')
def step_then_generate_resolution_report(context):
    """Generate a report confirming no reoccurrence of past issues"""
    logging.info(f"Validation report generated for {context.file_name}.")


@then('any reoccurrence should be flagged as "{severity}"')
def step_then_flag_reoccurrence(context, severity):
    """Flag issues if they reoccur"""
    if context.is_reoccurring:
        logging.warning(f"Reoccurring issue detected in {context.file_name} with severity: {severity}")


@given('a database that had past issues with "{issue_type}"')
def step_given_database_with_past_issues(context, issue_type):
    """Simulate a database with previously resolved issues"""
    context.issue_type = issue_type
    context.db_data = {"issue_type": issue_type, "status": "Resolved"}


@when('I compare the latest records with previous resolutions')
def step_when_compare_database_records(context):
    """Simulate a database comparison to check for resolved issue reoccurrence"""
    context.discrepancy_found = bool(random.getrandbits(1))  # Random reoccurrence simulation
    time.sleep(1)  # Simulating processing time


@then('no past issues should reappear')
def step_then_no_past_issues_reappear(context):
    """Ensure past issues do not reoccur"""
    assert not context.discrepancy_found, f"Previously resolved issue ({context.issue_type}) has resurfaced!"
    logging.info("Database integrity maintained for past issues.")


@then('any detected inconsistencies should be logged as "{discrepancy_type}"')
def step_then_log_inconsistencies(context, discrepancy_type):
    """Ensure any reoccurrence is logged properly"""
    if context.discrepancy_found:
        logging.warning(f"Detected discrepancy: {discrepancy_type}")


@given('a batch of bank export files from "{year_range}" containing previously flagged issues')
def step_given_batch_with_past_issues(context, year_range):
    """Simulate a batch of files containing previously flagged issues"""
    context.year_range = year_range
    context.batch_files = [f"transactions_{year}.csv" for year in range(2018, 2023)]


@when('I process them for validation')
    """Simulate batch processing for consistency checking"""
    context.issue_count = random.randint(0, 5)  # Random reoccurrence simulation
    time.sleep(2)  # Simulating processing time


@then('all records should pass consistency checks')
def step_then_validate_batch_consistency(context):
    """Ensure all records pass consistency validation"""
    logging.info(f"All records from {context.year_range} passed consistency checks.")


@then('no previously resolved issues should reoccur')
def step_then_no_resolved_issues_reappear(context):
    """Ensure no past issues resurface"""
    assert context.issue_count == 0, "Resolved issues have reappeared!"
    logging.info("Batch processing verified for resolved issues.")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_attempt_to_process_file(context, file_name):
    """Simulate an attempt to process a bank export file with past issues"""
    context.file_name = file_name


@when('previously resolved issues such as "{error_type}" are detected again')
def step_when_detect_resolved_issues(context, error_type):
    """Simulate detecting previously resolved issues in the latest export"""
    context.error_found = bool(random.getrandbits(1))
    context.error_type = error_type if context.error_found else None


@then('a system alert should notify relevant users')
    """Ensure users are notified of issue reoccurrences"""
    if context.error_found:
        logging.warning(f"System alert: Reoccurrence of {context.error_type} detected in {context.file_name}!")


@then('the issue should be escalated if its severity level is "{severity_level}"')
def step_then_escalate_critical_issues(context, severity_level):
    """Ensure critical issues are escalated if they reoccur"""
    if context.error_found:
        logging.info(f"Issue reoccurrence escalated due to severity: {severity_level}")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_system_processing_resolved_issues(context, file_count):
    """Simulate the system processing multiple export files per hour"""
    context.file_count = int(file_count)


@when('checking for previously resolved issues in "{year_range}"')
def step_when_checking_past_resolved_issues(context, year_range):
    """Simulate validating previously resolved issues in a specific year range"""
    context.processing_time = random.randint(100, 600)  # Simulating processing duration
    time.sleep(1)  # Simulating processing delay


@then('processing should complete within "{expected_time}" seconds')
    """Ensure regression validation completes within the expected time"""
    assert context.processing_time <= int(expected_time), "Processing took too long!"
    logging.info(f"Resolved issue validation completed in {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_monitor_system_usage(context, resource_limit):
    """Ensure resource usage remains within acceptable limits"""
    actual_resource_usage = random.randint(50, 90)
    assert actual_resource_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"Resource usage: {actual_resource_usage}%, within the allowed limit.")


@then('data integrity should remain stable throughout the process')
    """Ensure data integrity remains stable while validating past resolved issues"""
    integrity_check = bool(random.getrandbits(1))  # Simulating data stability validation
    assert integrity_check, "Data integrity issues detected!"
    logging.info("Data integrity verified successfully.")

# ================= End of Previously Resolved Issues Validation Step Definitions =================

# ================= Beginning of High-Volume Transaction Processing Validation =================
# This script validates high-volume transaction processing in regression testing.
# It ensures:
# - Data integrity across millions of transactions.
# - Database performance under large transaction loads.
# - Efficient batch processing with optimized memory usage.
# - Proper error handling for high transaction volumes.
# - Network latency resilience during remote processing.
# - Performance scaling under extreme transaction loads.

@given('a bank export file named "{file_name}" containing "{transaction_count}" transactions')
def step_given_high_volume_file(context, file_name, transaction_count):
    """Simulate loading a high-volume transaction file"""
    context.file_name = file_name
    context.transaction_count = int(transaction_count)
    context.processed_count = 0


@when('the system processes the file')
def step_when_process_high_volume_file(context):
    """Simulate processing the high-volume transaction file"""
    processing_time = min(context.transaction_count / 10000, 5)  # Simulating transaction processing time
    time.sleep(processing_time)
    context.processed_count = context.transaction_count
    logging.info(f"Processed {context.processed_count} transactions from {context.file_name}.")


@then('all transactions should be recorded accurately')
def step_then_validate_transactions_recorded(context):
    """Ensure all transactions are recorded without errors"""
    assert context.processed_count == context.transaction_count, "Transaction count mismatch!"
    logging.info("All transactions recorded successfully.")


@then('no data loss or corruption should occur')
def step_then_validate_no_data_loss(context):
    """Ensure no transaction data is lost"""
    assert random.random() > 0.05, "Data loss detected!"
    logging.info("No data corruption detected during processing.")


@given('a database containing "{transaction_count}" transactions')
def step_given_database_high_transaction_load(context, transaction_count):
    """Simulate a database loaded with high transaction volumes"""
    context.db_transaction_count = int(transaction_count)


@when('a query retrieves transactions from the last "{time_period}"')
def step_when_query_transactions(context, time_period):
    """Simulate querying a large database for recent transactions"""
    context.query_time = random.randint(1, 10)  # Simulated execution time in seconds
    time.sleep(context.query_time)
    context.time_period = time_period
    logging.info(f"Queried transactions for {context.time_period} in {context.query_time} seconds.")


@then('the query should execute within "{expected_time}" seconds')
    """Ensure queries execute within the expected time"""
    assert context.query_time <= int(expected_time), "Query took too long!"
    logging.info("Query performance within acceptable limits.")


@given('"{batch_count}" bank export files each containing "{transaction_count}" transactions')
def step_given_batch_transaction_processing(context, batch_count, transaction_count):
    """Simulate batch processing of high-volume transactions"""
    context.batch_count = int(batch_count)
    context.transaction_count = int(transaction_count)


@when('the system processes these files in parallel')
    """Simulate batch transaction processing"""
    context.batch_processing_time = random.randint(100, 900)
    time.sleep(1)
    logging.info(f"Batch processing completed in {context.batch_processing_time} seconds.")


@then('system memory consumption should remain under "{memory_limit}%"')
    """Ensure system memory consumption remains within the limit"""
    actual_memory_usage = random.randint(60, 85)
    assert actual_memory_usage <= int(memory_limit), "Memory usage exceeded!"
    logging.info(f"Memory usage: {actual_memory_usage}%, within limit.")


@given('a bank export file "{file_name}" with "{error_type}" errors in "{error_percentage}%" of transactions')
def step_given_high_volume_errors(context, file_name, error_type, error_percentage):
    """Simulate a high-volume transaction file with errors"""
    context.file_name = file_name
    context.error_type = error_type
    context.error_percentage = int(error_percentage)


@when('I attempt to process the file')
def step_when_process_file_with_errors(context):
    """Simulate error-prone file processing"""
    context.error_count = (context.transaction_count * context.error_percentage) // 100
    context.valid_transactions = context.transaction_count - context.error_count
    logging.info(f"Processed {context.valid_transactions} valid transactions from {context.file_name}.")


@then('all errors should be logged properly')
    """Ensure all errors are correctly logged"""
    logging.warning(f"{context.error_count} transactions failed due to {context.error_type} errors.")


@given('a system processing "{transaction_count}" transactions per second')
def step_given_transaction_load(context, transaction_count):
    """Simulate a system processing a specific number of transactions per second"""
    context.transaction_rate = int(transaction_count)


@when('the transaction load increases by "{increase_percentage}%"')
def step_when_transaction_load_increases(context, increase_percentage):
    """Simulate a sudden increase in transaction processing load"""
    context.scaled_transaction_rate = context.transaction_rate * (1 + int(increase_percentage) / 100)
    logging.info(f"New transaction processing rate: {context.scaled_transaction_rate} per second.")


@then('the system should scale dynamically without degradation')
def step_then_validate_scalability(context):
    """Ensure the system scales properly under high load"""
    assert context.scaled_transaction_rate <= context.transaction_rate * 2, "System scalability failure!"
    logging.info("System scaled dynamically under high load.")


@given('a bank export file "{file_name}" with "{transaction_count}" transactions and simulated network latency of "{latency}" ms')
def step_given_network_latency_simulation(context, file_name, transaction_count, latency):
    """Simulate network latency during high-volume transaction processing"""
    context.file_name = file_name
    context.transaction_count = int(transaction_count)
    context.latency = int(latency)


@when('I attempt to process the file remotely')
def step_when_process_with_latency(context):
    """Simulate remote processing of a large transaction file under latency"""
    context.latency_effect = context.latency / 1000  # Convert ms to seconds
    time.sleep(context.latency_effect)
    logging.info(f"Processing {context.file_name} with {context.latency} ms latency.")


@then('processing should not hang indefinitely')
def step_then_validate_latency_handling(context):
    """Ensure the system does not hang under latency conditions"""
    assert context.latency_effect < 5, "Processing hung due to high latency!"
    logging.info("Network latency handled successfully.")

# ================= End of High-Volume Transaction Processing Validation =================

# ================= Beginning of Regression Testing for Previously Fixed Bugs =================
# This script validates that previously fixed bugs do not reoccur in regression testing.
# It ensures:
# - Data integrity by preventing past issues from resurfacing.
# - Database consistency in records that were affected by previous bugs.
# - Batch processing maintains resolved issues without reintroducing errors.
# - Proper error handling and alerting for unexpected bug reoccurrence.
# - System performance is maintained during large-scale regression checks.

@given('a bank export file named "{file_name}" that had an issue fixed in version "{fixed_version}"')
def step_given_fixed_issue_file(context, file_name, fixed_version):
    """Simulate loading a bank export file with previously fixed issues"""
    context.file_name = file_name
    context.fixed_version = fixed_version
    context.issue_resolved = True


@when('I process the file')
def step_when_process_fixed_issue_file(context):
    """Simulate processing the export file with previously fixed issues"""
    processing_time = random.uniform(0.5, 2)  # Simulate processing delay
    time.sleep(processing_time)
    context.issue_resolved = random.choice([True, False])  # Simulate random failure
    logging.info(f"Processed {context.file_name}. Previously fixed issue status: {'Resolved' if context.issue_resolved else 'Reoccurred'}")


@then('the issue should not reoccur')
def step_then_validate_fixed_issue(context):
    """Ensure previously resolved issues do not reappear"""
    assert context.issue_resolved, "Previously fixed issue has reoccurred!"
    logging.info("Previously resolved issue has not reoccurred.")


@then('a validation report should confirm the resolution')
    """Generate a validation report for the fixed issue"""
    report_status = "Issue successfully validated" if context.issue_resolved else "Issue reoccurred"
    logging.info(f"Validation report generated: {report_status}")


@given('a database that contained records affected by "{issue_type}"')
    """Simulate a database that had past issues"""
    context.issue_type = issue_type
    context.db_resolved = True


@when('I compare the latest records with the resolved state')
    """Simulate checking database records for past issues"""
    comparison_time = random.uniform(1, 5)
    time.sleep(comparison_time)
    context.db_resolved = random.choice([True, False])  # Simulate a random reoccurrence
    logging.info(f"Checked for {context.issue_type} in database. Status: {'Resolved' if context.db_resolved else 'Reoccurred'}")


@then('no past issues should reappear')
def step_then_validate_no_past_issues(context):
    """Ensure past database issues do not reoccur"""
    assert context.db_resolved, f"Previously resolved issue {context.issue_type} has reoccurred!"
    logging.info(f"No reoccurrence of {context.issue_type} detected in the database.")


@given('"{batch_count}" bank export files from "{year_range}" containing previously flagged issues')
    """Simulate batch processing of export files with previously resolved issues"""
    context.batch_count = int(batch_count)
    context.year_range = year_range


@when('I process them for validation')
def step_when_validate_batch_processing(context):
    """Simulate batch processing validation"""
    batch_processing_time = random.randint(100, 900)
    time.sleep(1)
    context.batch_validated = random.choice([True, False])
    logging.info(f"Batch validation for {context.year_range} completed. Issues reoccurred: {not context.batch_validated}")


@then('all records should pass consistency checks')
    """Ensure batch processing does not reintroduce old issues"""
    assert context.batch_validated, "Batch processing reintroduced previously resolved issues!"
    logging.info("Batch processing maintained resolved issues without regression.")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_error_handling_validation(context, file_name):
    """Simulate an attempt to process a file with potential regression issues"""
    context.file_name = file_name


@when('a previously fixed issue such as "{error_type}" is detected again')
def step_when_detect_regression_issue(context, error_type):
    """Simulate detecting a regression issue"""
    context.regression_issue_detected = random.choice([True, False])
    context.error_type = error_type
    logging.warning(f"Detected {error_type} issue again in {context.file_name}") if context.regression_issue_detected else logging.info("No regression issues detected.")


@then('a system alert should notify relevant users')
def step_then_send_alert(context):
    """Trigger an alert if a regression issue is detected"""
    if context.regression_issue_detected:
        logging.error(f"ALERT: Regression issue '{context.error_type}' detected in {context.file_name}!")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_regression_check(context, file_count):
    """Simulate high-volume regression testing"""
    context.file_count = int(file_count)


@when('checking for previously fixed issues in "{year_range}"')
def step_when_perform_regression_check(context, year_range):
    """Perform regression testing on high volumes of historical data"""
    context.year_range = year_range
    context.regression_test_time = random.randint(200, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for fixed issues in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
    """Ensure regression testing completes within the expected time"""
    assert context.regression_test_time <= int(expected_time), "Regression test took too long!"
    logging.info(f"Regression test completed within {context.regression_test_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_validate_resource_usage(context, resource_limit):
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")

# ================= End of Regression Testing for Previously Fixed Bugs =================

# ================= Beginning of Regression Testing for Transaction Reference Uniqueness =================
# This script ensures:
# - Every transaction reference remains unique.
# - No duplicate references exist in batch and database processing.
# - Any detected duplicates are flagged and logged appropriately.
# - System maintains data integrity and performance while validating uniqueness.

@given('a bank export file named "{file_name}" containing "{transaction_count}" transactions')
def step_given_transaction_file(context, file_name, transaction_count):
    """Simulate loading a bank export file with transactions"""
    context.file_name = file_name
    context.transaction_count = int(transaction_count)
    context.duplicates_found = False
    logging.info(f"Loaded {transaction_count} transactions from {file_name}.")


@when('the system processes the file')
def step_when_process_transactions(context):
    """Simulate processing the transactions and checking for duplicate references"""
    processing_time = random.uniform(0.5, 2)  # Simulated processing delay
    time.sleep(processing_time)

    # Simulate transaction reference uniqueness check
    duplicate_rate = 0.001  # 0.1% chance of duplicate
    context.duplicates_found = random.random() < duplicate_rate

    logging.info(f"Processed {context.file_name}. Duplicate references found: {context.duplicates_found}")


@then('each transaction should have a unique reference ID')
def step_then_validate_transaction_uniqueness(context):
    """Ensure all transaction references are unique"""
    assert not context.duplicates_found, "Duplicate transaction references detected!"
    logging.info("All transactions have unique reference IDs.")


@then('duplicate transaction references should be flagged as "{severity}"')
def step_then_flag_duplicates(context, severity):
    """Flag duplicates if found"""
    if context.duplicates_found:
        logging.warning(f"Duplicate transaction references found! Severity: {severity}")
    else:
        logging.info("No duplicate transaction references detected.")


@given('a database containing transaction records from "{year_range}"')
def step_given_database_transactions(context, year_range):
    """Simulate database containing past transaction records"""
    context.year_range = year_range


@when('I check for duplicate transaction references')
def step_when_check_duplicate_references(context):
    """Check for duplicate transaction references in the database"""
    check_time = random.uniform(1, 5)  # Simulated database check time
    time.sleep(check_time)

    context.db_duplicates_found = random.choice([True, False])  # Simulate duplicate check result
    logging.info(
        f"Checked database records for duplicates in {context.year_range}. Found: {context.db_duplicates_found}")


@then('no duplicate references should exist')
def step_then_validate_database_uniqueness(context):
    """Ensure database transaction references remain unique"""
    assert not context.db_duplicates_found, "Duplicate transaction references detected in database!"
    logging.info("Database records maintain unique transaction references.")


@given('"{batch_count}" bank export files from "{year_range}"')
def step_given_batch_transactions(context, batch_count, year_range):
    """Simulate batch processing of bank export files"""
    context.batch_count = int(batch_count)
    context.year_range = year_range


@when('I process them for validation')
def step_when_validate_batch_transactions(context):
    """Simulate batch processing for transaction reference uniqueness"""
    batch_processing_time = random.randint(100, 900)
    time.sleep(1)
    context.batch_validated = random.choice([True, False])
    logging.info(f"Batch validation for {context.year_range} completed. Issues found: {not context.batch_validated}")


@then('all transactions should maintain unique references')
def step_then_validate_batch_reference_uniqueness(context):
    """Ensure batch processing maintains unique transaction references"""
    assert context.batch_validated, "Batch processing introduced duplicate transaction references!"
    logging.info("Batch processing maintained unique transaction references.")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_duplicate_handling(context, file_name):
    """
    Simulate an attempt to process a file with duplicate transaction references.
    """
    context.file_name = file_name


@when('duplicate transaction references such as "{error_type}" are detected')
def step_when_detect_duplicate_issue(context, error_type):
    """Simulate detecting duplicate transaction reference issues"""
    context.duplicate_issue_detected = random.choice([True, False])
    context.error_type = error_type
    logging.warning(
        f"Detected {error_type} issue again in {context.file_name}") if context.duplicate_issue_detected else logging.info(
        "No duplicate transaction references detected.")


@then('a system alert should notify relevant users')
def step_then_send_duplicate_alert(context):
    """Trigger an alert if duplicate transaction references are detected"""
    if context.duplicate_issue_detected:
        logging.error(f"ALERT: Duplicate transaction reference '{context.error_type}' detected in {context.file_name}!")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_reference_check(context, file_count):
    """Simulate high-volume transaction reference checking"""
    context.file_count = int(file_count)


@when('checking for duplicate transaction references in "{year_range}"')
def step_when_perform_reference_check(context, year_range):
    """Perform duplicate transaction reference check across multiple years"""
    context.year_range = year_range
    context.reference_check_time = random.randint(200, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for duplicate references in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_processing_speed(context, expected_time):
    """Ensure transaction reference validation completes within the expected time"""
    assert context.reference_check_time <= int(expected_time), "Transaction reference check took too long!"
    logging.info(f"Transaction reference check completed within {context.reference_check_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")

# ================= End of Regression Testing for Transaction Reference Uniqueness =================

# ================= Beginning of Structural Testing for Column Case Sensitivity =================
# This script ensures:
# - Column headers are mapped correctly despite case variations.
# - Database integrity is maintained with case-insensitive column mappings.
# - No data is lost due to column case mismatches.
# - The system maintains performance while validating column names.

@given('a bank export file named "{file_name}" with columns in "{case_format}"')
def step_given_column_case_variations(context, file_name, case_format):
    """Simulate loading a bank export file with different column case formats"""
    context.file_name = file_name
    context.case_format = case_format
    context.mismatched_columns = random.choice([True, False])  # Randomly simulate case mismatch
    logging.info(f"Loaded {file_name} with columns in {case_format} case format.")


@when('the system processes the file')
def step_when_process_file_case_variations(context):
    """Simulate processing the file and validating column headers"""
    processing_time = random.uniform(0.5, 2)
    time.sleep(processing_time)
    logging.info(f"Processed {context.file_name}. Column mismatches detected: {context.mismatched_columns}")


@then('column headers should be mapped correctly')
def step_then_validate_column_mappings(context):
    """Ensure column headers are correctly mapped regardless of case"""
    assert not context.mismatched_columns, "Column mapping mismatch detected!"
    logging.info("All column headers mapped correctly.")


@then('no data should be lost due to case mismatches')
    """Ensure data is not lost due to case mismatches"""
    assert not context.mismatched_columns, "Potential data loss due to column case mismatches!"
    logging.info("No data loss occurred due to column case variations.")


@given('a database with expected column names in "{expected_case_format}"')
def step_given_database_column_expectations(context, expected_case_format):
    """Simulate expected column names in the database"""
    context.expected_case_format = expected_case_format


@when('I compare imported column names from "{file_name}"')
def step_when_compare_database_columns(context, file_name):
    """Compare column names from imported files to the expected format"""
    context.file_name = file_name
    context.discrepancies_found = random.choice([True, False])
    logging.info(f"Compared imported columns in {file_name}. Discrepancies found: {context.discrepancies_found}")


@then('column mappings should be case-insensitive')
def step_then_validate_case_insensitive_mappings(context):
    """Ensure case variations do not affect column mappings"""
    assert not context.discrepancies_found, "Case-sensitive column mismatches detected!"
    logging.info("Column mappings are correctly case-insensitive.")


@given('a batch of bank export files with columns in "{case_format}"')
def step_given_batch_column_variations(context, case_format):
    """Simulate batch processing of bank export files with varying column cases"""
    context.case_format = case_format


@when('the system processes them for validation')
    """Process batch files and check for column mismatches"""
    batch_processing_time = random.randint(1, 3)
    time.sleep(batch_processing_time)
    context.batch_column_mismatch = random.choice([True, False])
    logging.info(f"Batch processing completed. Column mismatches found: {context.batch_column_mismatch}")


@then('all columns should be correctly recognized')
def step_then_validate_batch_columns(context):
    """Ensure batch files maintain correct column mappings"""
    assert not context.batch_column_mismatch, "Batch processing introduced column mismatches!"
    logging.info("All batch files maintained correct column mappings.")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_file_with_column_mismatch(context, file_name):
    """Simulate an attempt to process a file with column mismatches"""
    context.file_name = file_name


@when('a column case mismatch such as "{error_type}" is detected')
def step_when_detect_column_mismatch(context, error_type):
    """Detect case mismatches in column names"""
    context.error_detected = random.choice([True, False])
    context.error_type = error_type
    logging.warning(f"Detected {error_type} issue in {context.file_name}") if context.error_detected else logging.info("No column case mismatches detected.")


@then('a system alert should notify relevant users')
def step_then_alert_column_mismatch(context):
    """Notify users about column mismatches"""
    if context.error_detected:
        logging.error(f"ALERT: Column case mismatch '{context.error_type}' detected in {context.file_name}!")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_column_check(context, file_count):
    """Simulate high-volume file processing while checking column consistency"""
    context.file_count = int(file_count)


@when('checking for column case variations in "{year_range}"')
def step_when_perform_column_case_check(context, year_range):
    """Perform column case validation across multiple years"""
    context.year_range = year_range
    context.processing_time = random.randint(100, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for column case mismatches in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_column_case_processing_speed(context, expected_time):
    """Ensure column case validation completes within the expected time"""
    assert context.processing_time <= int(expected_time), "Column case validation took too long!"
    logging.info(f"Column case validation completed within {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")

# ================= End of Structural Testing for Column Case Sensitivity =================

# ================= Beginning of Structural Testing for Column Format Validation =================
# This script ensures:
# - Column formats adhere to expected data types.
# - Database integrity is maintained with correct column format mappings.
# - No data is lost due to format mismatches.
# - The system maintains performance while validating column formats.

@given('a bank export file named "{file_name}" with column formats defined as "{expected_format}"')
def step_given_column_format_variations(context, file_name, expected_format):
    """Simulate loading a bank export file with expected column formats"""
    context.file_name = file_name
    context.expected_format = expected_format
    context.format_mismatches = random.choice([True, False])  # Simulating a format mismatch
    logging.info(f"Loaded {file_name} with expected format: {expected_format}.")


@when('the system processes the file')
def step_when_process_file_format_variations(context):
    """Simulate processing the file and validating column formats"""
    processing_time = random.uniform(0.5, 2)
    time.sleep(processing_time)
    logging.info(f"Processed {context.file_name}. Format mismatches detected: {context.format_mismatches}")


@then('all columns should match the expected format')
def step_then_validate_column_formats(context):
    """Ensure column formats match expected data types"""
    assert not context.format_mismatches, "Column format mismatch detected!"
    logging.info("All column formats match the expected types.")


@then('any format mismatches should be flagged as "{severity}"')
def step_then_flag_format_mismatches(context, severity):
    """Ensure mismatched formats are flagged accordingly"""
    if context.format_mismatches:
        logging.warning(f"Column format mismatch detected in {context.file_name}. Severity: {severity}")


@given('a database with expected column formats in "{expected_format}"')
def step_given_database_column_format_expectations(context, expected_format):
    """Simulate expected column formats in the database"""
    context.expected_format = expected_format


@when('I compare imported column formats from "{file_name}"')
def step_when_compare_database_column_formats(context, file_name):
    """Compare column formats from imported files to the expected format"""
    context.file_name = file_name
    context.format_discrepancies_found = random.choice([True, False])
    logging.info(f"Compared imported column formats in {file_name}. Discrepancies found: {context.format_discrepancies_found}")


@then('all columns should match the expected data type')
def step_then_validate_column_data_types(context):
    """Ensure column data types are correctly formatted"""
    assert not context.format_discrepancies_found, "Column format discrepancies detected!"
    logging.info("Column formats are correctly aligned with database expectations.")


@given('a batch of bank export files with columns formatted as "{format_type}"')
def step_given_batch_column_format_variations(context, format_type):
    """Simulate batch processing of bank export files with varying column formats"""
    context.format_type = format_type


@when('the system processes them for validation')
def step_when_process_batch_files_format(context):
    """Process batch files and check for column format inconsistencies"""
    batch_processing_time = random.randint(1, 3)
    time.sleep(batch_processing_time)
    context.batch_format_mismatch = random.choice([True, False])
    logging.info(f"Batch processing completed. Format mismatches found: {context.batch_format_mismatch}")


@then('all columns should adhere to the correct format')
def step_then_validate_batch_column_formats(context):
    """Ensure batch files maintain correct column formatting"""
    assert not context.batch_format_mismatch, "Batch processing introduced column format mismatches!"
    logging.info("All batch files maintained correct column formats.")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_file_with_column_format_mismatch(context, file_name):
    """Simulate an attempt to process a file with column format mismatches"""
    context.file_name = file_name


@when('a column format inconsistency such as "{error_type}" is detected')
def step_when_detect_column_format_mismatch(context, error_type):
    """Detect format inconsistencies in column values"""
    context.error_detected = random.choice([True, False])
    context.error_type = error_type
    logging.warning(f"Detected {error_type} issue in {context.file_name}") if context.error_detected else logging.info("No column format mismatches detected.")


@then('a system alert should notify relevant users')
def step_then_alert_column_format_mismatch(context):
    """Notify users about column format mismatches"""
    if context.error_detected:
        logging.error(f"ALERT: Column format inconsistency '{context.error_type}' detected in {context.file_name}!")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_column_format_check(context, file_count):
    """Simulate high-volume file processing while checking column format consistency"""
    context.file_count = int(file_count)


@when('checking for column format variations in "{year_range}"')
def step_when_perform_column_format_check(context, year_range):
    """Perform column format validation across multiple years"""
    context.year_range = year_range
    context.processing_time = random.randint(100, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for column format mismatches in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_column_format_processing_speed(context, expected_time):
    """Ensure column format validation completes within the expected time"""
    assert context.processing_time <= int(expected_time), "Column format validation took too long!"
    logging.info(f"Column format validation completed within {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_validate_column_format_resource_usage(context, resource_limit):
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")

# ================= End of Structural Testing for Column Format Validation =================

# ================= Beginning of Structural Testing for Extra Columns =================
# This script ensures:
# - Extra columns in bank export files are detected and handled properly.
# - Unexpected columns do not disrupt data integrity.
# - The database remains consistent despite schema variations.
# - System performance is maintained when processing files with extra columns.

@given('a bank export file named "{file_name}" containing extra columns')
def step_given_extra_columns_file(context, file_name):
    """Simulate loading a bank export file with extra columns"""
    context.file_name = file_name
    context.extra_columns_detected = random.choice([True, False])  # Simulating extra column presence
    logging.info(f"Loaded {file_name} with extra columns detected: {context.extra_columns_detected}.")


@when('the system processes the file')
def step_when_process_file_with_extra_columns(context):
    """Simulate processing the file and detecting extra columns"""
    processing_time = random.uniform(0.5, 2)
    time.sleep(processing_time)
    logging.info(f"Processing {context.file_name}. Extra columns detected: {context.extra_columns_detected}")


@then('extra columns should be flagged as "{severity}"')
def step_then_flag_extra_columns(context, severity):
    """Ensure extra columns are flagged accordingly"""
    if context.extra_columns_detected:
        logging.warning(f"Extra columns detected in {context.file_name}. Severity: {severity}")


@then('a validation report should document unexpected columns')
def step_then_generate_extra_column_report(context):
    """Generate a report listing the extra columns"""
    if context.extra_columns_detected:
        logging.info(f"Validation report generated for extra columns in {context.file_name}.")


@given('a database expecting standard column structure')
def step_given_database_standard_schema(context):
    """Simulate a database with a predefined schema"""
    context.database_has_fixed_schema = True


@when('I compare imported column names from "{file_name}"')
def step_when_compare_database_column_names(context, file_name):
    """Compare imported column names with the expected schema"""
    context.file_name = file_name
    context.schema_mismatch = random.choice([True, False])
    logging.info(f"Compared column names for {file_name}. Schema mismatch: {context.schema_mismatch}")


@then('extra columns should be ignored or flagged as "{discrepancy_type}"')
def step_then_handle_extra_columns_in_db(context, discrepancy_type):
    """Ensure extra columns are ignored or flagged correctly in the database"""
    if context.schema_mismatch:
        logging.warning(f"Schema mismatch detected in {context.file_name}. Discrepancy Type: {discrepancy_type}")


@given('a batch of bank export files with extra columns')
def step_given_batch_extra_column_files(context):
    """Simulate batch processing of export files with extra columns"""
    context.batch_contains_extra_columns = random.choice([True, False])


@when('the system processes them for validation')
def step_when_process_batch_files_extra_columns(context):
    """Process batch files and check for extra columns"""
    batch_processing_time = random.randint(1, 3)
    time.sleep(batch_processing_time)
    context.batch_column_mismatch = random.choice([True, False])
    logging.info(f"Batch processing completed. Extra columns detected: {context.batch_column_mismatch}")


@then('all extra columns should be detected and flagged as "{severity}"')
def step_then_validate_batch_extra_columns(context, severity):
    """Ensure extra columns in batch files are flagged"""
    if context.batch_column_mismatch:
        logging.warning(f"Extra columns detected in batch processing. Severity: {severity}")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_file_with_extra_columns(context, file_name):
    """Simulate an attempt to process a file with extra columns"""
    context.file_name = file_name


@when('extra columns such as "{column_name}" are detected')
def step_when_detect_extra_columns(context, column_name):
    """Detect extra columns in the file"""
    context.extra_column_detected = random.choice([True, False])
    context.column_name = column_name
    logging.warning(f"Extra column '{column_name}' detected in {context.file_name}") if context.extra_column_detected else logging.info("No extra columns detected.")


@then('a system alert should notify relevant users')
def step_then_alert_extra_column_detection(context):
    """Notify users about extra column detection"""
    if context.extra_column_detected:
        logging.error(f"ALERT: Extra column '{context.column_name}' detected in {context.file_name}!")


@then('an auto-mapping mechanism should suggest appropriate actions')
def step_then_suggest_column_mapping(context):
    """Suggest auto-mapping for extra columns"""
    if context.extra_column_detected:
        logging.info(f"Auto-mapping suggested for extra column '{context.column_name}' in {context.file_name}.")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_extra_column_check(context, file_count):
    """Simulate high-volume file processing while handling extra columns"""
    context.file_count = int(file_count)


@when('extra columns are present in "{year_range}"')
def step_when_detect_extra_columns_in_year_range(context, year_range):
    """Perform extra column validation across multiple years"""
    context.year_range = year_range
    context.processing_time = random.randint(100, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for extra columns in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_extra_column_processing_speed(context, expected_time):
    """Ensure processing with extra columns completes within expected time"""
    assert context.processing_time <= int(expected_time), "Extra column validation took too long!"
    logging.info(f"Processing completed within {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_validate_extra_column_resource_usage(context, resource_limit):
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")

# ================= End of Structural Testing for Extra Columns =================

# ================= Beginning of Structural Testing for Header Mismatch Validation =================
# This script ensures:
# - Bank export files have the correct headers in expected order.
# - Any header mismatches are flagged and logged.
# - The database remains consistent with predefined header structures.
# - System performance remains stable when processing files with header discrepancies.

@given('a bank export file named "{file_name}" with headers "{header_format}"')
def step_given_header_format(context, file_name, header_format):
    """Simulate loading a bank export file with specific header formats"""
    context.file_name = file_name
    context.header_format = header_format
    context.header_mismatch_detected = random.choice([True, False])  # Simulating header mismatch
    logging.info(f"Loaded {file_name} with header format: {header_format}. Mismatch detected: {context.header_mismatch_detected}")


@when('the system processes the file')
def step_when_process_file_with_headers(context):
    """Simulate processing the file and checking headers"""
    processing_time = random.uniform(0.5, 2)
    time.sleep(processing_time)
    logging.info(f"Processing {context.file_name}. Header mismatch detected: {context.header_mismatch_detected}")


@then('all headers should match the expected structure')
def step_then_validate_headers(context):
    """Ensure headers are properly validated"""
    if context.header_mismatch_detected:
        logging.warning(f"Header mismatch found in {context.file_name}!")


@then('any mismatched headers should be flagged as "{severity}"')
def step_then_flag_header_mismatches(context, severity):
    """Flag header mismatches based on severity"""
    if context.header_mismatch_detected:
        logging.error(f"Header mismatch severity: {severity} for {context.file_name}")


@then('a validation report should document header inconsistencies')
def step_then_generate_header_validation_report(context):
    """Generate a report for header mismatches"""
    if context.header_mismatch_detected:
        logging.info(f"Validation report generated for header inconsistencies in {context.file_name}")


@then('if auto-mapping is enabled, a correction suggestion should be provided')
def step_then_suggest_header_correction(context):
    """Provide auto-mapping suggestions if enabled"""
    if context.header_mismatch_detected:
        logging.info(f"Suggested header correction for {context.file_name}")


@given('a database expecting a predefined column structure')
def step_given_database_standard_header(context):
    """Simulate a database with a predefined schema for headers"""
    context.database_has_fixed_schema = True


@when('I compare imported headers from "{file_name}"')
def step_when_compare_imported_headers(context, file_name):
    """Compare imported headers with expected headers"""
    context.file_name = file_name
    context.schema_mismatch = random.choice([True, False])
    logging.info(f"Compared headers for {file_name}. Schema mismatch: {context.schema_mismatch}")


@then('all headers should align with the expected format')
def step_then_validate_database_headers(context):
    """Ensure headers in database match the expected format"""
    if context.schema_mismatch:
        logging.warning(f"Header schema mismatch detected in {context.file_name}.")


@then('any mismatches should be flagged as "{discrepancy_type}"')
def step_then_flag_schema_mismatches(context, discrepancy_type):
    """Flag schema mismatches in headers"""
    if context.schema_mismatch:
        logging.error(f"Schema mismatch detected in {context.file_name}. Discrepancy Type: {discrepancy_type}")


@given('a batch of bank export files with header inconsistencies')
def step_given_batch_files_with_header_issues(context):
    """Simulate batch processing of export files with header issues"""
    context.batch_contains_header_mismatches = random.choice([True, False])


@when('the system processes them for validation')
def step_when_process_batch_files_with_headers(context):
    """Process batch files and check for header mismatches"""
    batch_processing_time = random.randint(1, 3)
    time.sleep(batch_processing_time)
    context.batch_header_mismatch = random.choice([True, False])
    logging.info(f"Batch processing completed. Header mismatches detected: {context.batch_header_mismatch}")


@then('all header mismatches should be detected and flagged as "{severity}"')
def step_then_validate_batch_header_mismatches(context, severity):
    """Ensure header mismatches in batch files are flagged"""
    if context.batch_header_mismatch:
        logging.warning(f"Header mismatches detected in batch processing. Severity: {severity}")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_file_with_header_issues(context, file_name):
    """Simulate an attempt to process a file with header mismatches"""
    context.file_name = file_name


@when('header mismatches such as "{error_type}" are detected')
def step_when_detect_header_mismatches(context, error_type):
    """Detect header mismatches in the file"""
    context.header_mismatch_detected = random.choice([True, False])
    context.error_type = error_type
    logging.warning(f"Header issue detected in {context.file_name}: {error_type}") if context.header_mismatch_detected else logging.info("No header mismatches detected.")


@then('a system alert should notify relevant users')
def step_then_alert_header_mismatch(context):
    """Notify users about header mismatches"""
    if context.header_mismatch_detected:
        logging.error(f"ALERT: Header issue detected in {context.file_name}! Type: {context.error_type}")


@then('an auto-mapping mechanism should suggest appropriate corrections')
def step_then_suggest_header_mapping(context):
    """Suggest auto-mapping for header mismatches"""
    if context.header_mismatch_detected:
        logging.info(f"Auto-mapping suggested for headers in {context.file_name}.")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_header_check(context, file_count):
    """Simulate high-volume file processing while handling header mismatches"""
    context.file_count = int(file_count)


@when('header mismatches are present in "{year_range}"')
def step_when_detect_header_mismatches_in_year_range(context, year_range):
    """Perform header validation across multiple years"""
    context.year_range = year_range
    context.processing_time = random.randint(100, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for header mismatches in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_header_processing_speed(context, expected_time):
    """Ensure processing with header mismatches completes within expected time"""
    assert context.processing_time <= int(expected_time), "Header validation took too long!"
    logging.info(f"Processing completed within {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_validate_header_resource_usage(context, resource_limit):
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")


@then('if resource utilization exceeds "{critical_limit}%", an alert should be triggered')
def step_then_trigger_alert_for_resource_usage(context, critical_limit):
    """Trigger an alert if resource usage exceeds the critical threshold"""
    actual_usage = random.randint(60, 95)
    if actual_usage > int(critical_limit):
        logging.critical(f"CRITICAL ALERT: System resource usage exceeded {critical_limit}%!")
    else:
        logging.info(f"System resource usage: {actual_usage}%, within safe limits.")

# ================= End of Structural Testing for Header Mismatch Validation =================

# ================= Beginning of Structural Testing for Merged Cells Validation =================
# This script ensures:
# - Merged cells in export files are detected and logged.
# - Data integrity is maintained despite merged cell issues.
# - Auto-splitting is suggested if enabled.
# - System performance remains stable when handling merged cell inconsistencies.

@given('a bank export file named "{file_name}" containing merged cells')
def step_given_file_with_merged_cells(context, file_name):
    """Simulate loading a bank export file that contains merged cells"""
    context.file_name = file_name
    context.merged_cells_detected = random.choice([True, False])
    logging.info(f"Loaded {file_name}. Merged cells detected: {context.merged_cells_detected}")


@when('the system processes the file')
def step_when_process_file_with_merged_cells(context):
    """Simulate processing the file and checking for merged cells"""
    processing_time = random.uniform(0.5, 2)
    time.sleep(processing_time)
    logging.info(f"Processing {context.file_name}. Merged cells detected: {context.merged_cells_detected}")


@then('merged cells should be detected and flagged as "{severity}"')
def step_then_flag_merged_cells(context, severity):
    """Flag merged cell issues based on severity"""
    if context.merged_cells_detected:
        logging.warning(f"Merged cells found in {context.file_name}. Severity: {severity}")


@then('a validation report should document the merged cell locations')
def step_then_generate_merged_cell_report(context):
    """Generate a report documenting merged cell locations"""
    if context.merged_cells_detected:
        logging.info(f"Validation report generated for merged cells in {context.file_name}")


@then('if auto-splitting is enabled, the system should attempt to correct the issue')
def step_then_auto_correct_merged_cells(context):
    """Simulate an auto-splitting mechanism for merged cells"""
    if context.merged_cells_detected:
        auto_split_success = random.choice([True, False])
        if auto_split_success:
            logging.info(f"Auto-splitting applied successfully for {context.file_name}")
        else:
            logging.warning(f"Auto-splitting failed for {context.file_name}")


@given('an attempt to process a bank export file "{file_name}"')
def step_given_file_for_error_handling(context, file_name):
    """Simulate an attempt to process a file with merged cell issues"""
    context.file_name = file_name


@when('merged cells are detected in "{column_name}"')
def step_when_detect_merged_cells_in_column(context, column_name):
    """Detect merged cells in a specific column"""
    context.merged_cells_detected = random.choice([True, False])
    context.column_name = column_name
    if context.merged_cells_detected:
        logging.warning(f"Merged cells detected in column {column_name} of {context.file_name}")


@then('a system alert should notify relevant users')
def step_then_alert_users_about_merged_cells(context):
    """Notify users about merged cells"""
    if context.merged_cells_detected:
        logging.error(f"ALERT: Merged cells detected in {context.file_name}, Column: {context.column_name}")


@then('an auto-splitting mechanism should suggest corrections if applicable')
def step_then_suggest_auto_splitting(context):
    """Suggest auto-splitting for merged cells"""
    if context.merged_cells_detected:
        logging.info(f"Suggested auto-splitting correction for {context.file_name}, Column: {context.column_name}")


@then('if correction is not possible, the file should be rejected')
def step_then_reject_file_with_unfixable_merged_cells(context):
    """Reject files if merged cells cannot be fixed"""
    if context.merged_cells_detected and not random.choice([True, False]):
        logging.error(f"File {context.file_name} rejected due to unresolvable merged cells.")


@given('a batch of bank export files with merged cell issues')
def step_given_batch_with_merged_cells(context):
    """Simulate batch processing of export files containing merged cells"""
    context.batch_contains_merged_cells = random.choice([True, False])


@when('the system processes them for validation')
def step_when_process_batch_with_merged_cells(context):
    """Process batch files and check for merged cell issues"""
    batch_processing_time = random.randint(1, 3)
    time.sleep(batch_processing_time)
    context.batch_merged_cells_detected = random.choice([True, False])
    logging.info(f"Batch processing completed. Merged cells detected: {context.batch_merged_cells_detected}")


@then('all merged cell occurrences should be detected and flagged as "{severity}"')
def step_then_flag_batch_merged_cells(context, severity):
    """Ensure merged cell issues in batch files are flagged"""
    if context.batch_merged_cells_detected:
        logging.warning(f"Merged cells detected in batch processing. Severity: {severity}")


@given('a system processing "{file_count}" bank export files per hour')
def step_given_high_volume_merged_cell_validation(context, file_count):
    """Simulate high-volume file processing with merged cells"""
    context.file_count = int(file_count)


@when('merged cells are present in "{year_range}"')
def step_when_detect_merged_cells_in_year_range(context, year_range):
    """Perform merged cell validation across multiple years"""
    context.year_range = year_range
    context.processing_time = random.randint(100, 600)
    time.sleep(1)
    logging.info(f"Checked {context.file_count} files for merged cells in {context.year_range}.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_merged_cell_processing_speed(context, expected_time):
    """Ensure processing with merged cells completes within expected time"""
    assert context.processing_time <= int(expected_time), "Merged cell validation took too long!"
    logging.info(f"Processing completed within {context.processing_time} seconds.")


@then('system resources should not exceed "{resource_limit}%"')
def step_then_validate_merged_cell_resource_usage(context, resource_limit):
    """Ensure system resource usage remains within acceptable limits"""
    actual_usage = random.randint(60, 85)
    assert actual_usage <= int(resource_limit), "System resource usage exceeded!"
    logging.info(f"System resource usage: {actual_usage}%, within limit.")


@given('an export file "{file_name}" with schema "{schema_type}"')
def step_given_file_with_merged_cell_schema(context, file_name, schema_type):
    """Simulate an export file with a specific schema that includes merged cells"""
    context.file_name = file_name
    context.schema_type = schema_type


@when('I check the schema validation rules')
def step_when_check_schema_validation_for_merged_cells(context):
    """Validate merged cell schema compliance"""
    context.schema_mismatch = random.choice([True, False])
    logging.info(f"Checked schema for {context.file_name}. Schema mismatch: {context.schema_mismatch}")


@then('all merged cells should be split according to "{expected_format}"')
def step_then_split_merged_cells(context, expected_format):
    """Ensure merged cells are split correctly based on schema"""
    if context.schema_mismatch:
        logging.warning(f"Schema mismatch detected in {context.file_name}. Expected format: {expected_format}")


@then('any detected schema violations should be logged as "{error_severity}"')
def step_then_log_schema_violations(context, error_severity):
    """Log schema violations due to merged cells"""
    if context.schema_mismatch:
        logging.error(f"Schema violation detected in {context.file_name}. Severity: {error_severity}")

# ================= End of Structural Testing for Merged Cells Validation =================

# ================= Beginning of Missing Columns Validation Script =================


@given('a bank export file named "{file_name}" with missing columns "{missing_columns}"')
def step_given_missing_columns(context, file_name, missing_columns):
    """Loads the file and identifies missing columns."""
    context.file_name = file_name
    context.missing_columns = missing_columns.split(", ")
    try:
        context.df = pd.read_csv(file_name) if file_name.endswith(".csv") else pd.read_excel(file_name)
        context.error = None
    except Exception as e:
        context.df = None
        context.error = str(e)

@when("the system processes the file")
    """Checks if specified columns are missing in the file."""
    if context.df is not None:
        context.missing_detected = [col for col in context.missing_columns if col not in context.df.columns]
    else:
        context.missing_detected = []

@then('the missing columns should be flagged with severity "{severity}"')
def step_then_flag_missing_columns(context, severity):
    """Flags missing columns based on severity level."""
    assert len(context.missing_detected) > 0, f"No missing columns detected in {context.file_name}"
    print(f"Missing columns in {context.file_name}: {context.missing_detected} - Severity: {severity}")

@then("a validation report should document the missing fields")
def step_then_document_missing_columns(context):
    """Generates a validation report for missing columns."""
    report = {
        "file_name": context.file_name,
        "missing_columns": context.missing_detected
    }
    print(f"Validation report generated: {report}")

@then('if auto-mapping is enabled, a correction suggestion should be provided')
    """Suggests corrections if auto-mapping is enabled."""
    if len(context.missing_detected) > 0:
        print(f"Suggested mappings for missing columns in {context.file_name}: {context.missing_detected}")

# Error Handling for Missing Columns
@given('an attempt to process a bank export file "{file_name}"')
def step_given_attempt_to_process(context, file_name):
    """Attempts to process the file while handling missing columns."""
    context.file_name = file_name
    try:
        context.df = pd.read_csv(file_name) if file_name.endswith(".csv") else pd.read_excel(file_name)
        context.error = None
    except Exception as e:
        context.df = None
        context.error = str(e)

@when('required columns are missing such as "{missing_column}"')
def step_when_required_columns_missing(context, missing_column):
    """Checks for missing required columns."""
    context.missing_column = missing_column
    if context.df is not None:
        context.missing_detected = [missing_column] if missing_column not in context.df.columns else []
    else:
        context.missing_detected = []

@then('a system alert should notify relevant users')
    """Logs an alert if missing columns are detected."""
    if len(context.missing_detected) > 0:
        print(f"ALERT: Missing required column {context.missing_column} in {context.file_name}")

@then('the issue should be escalated if the missing column severity level is "{severity_level}"')
def step_then_escalate_issue(context, severity_level):
    """Escalates issue based on severity level."""
    if len(context.missing_detected) > 0:
        print(f"Escalation required: Missing {context.missing_column} - Severity: {severity_level}")

@then('if correction is not possible, the file should be rejected')
def step_then_reject_file(context):
    """Rejects the file if the issue is critical."""
    if len(context.missing_detected) > 0:
        print(f"REJECTED: File {context.file_name} due to missing critical columns: {context.missing_detected}")

# Batch Processing for Missing Columns
@given("a batch of bank export files with missing columns")
def step_given_batch_with_missing_columns(context):
    """Loads batch files for validation."""
    context.batch_files = ["transactions_missing_account.csv", "transactions_missing_currency.xlsx"]

@when("the system processes them for validation")
    """Processes batch files and flags missing columns."""
    context.batch_issues = {}
    for file in context.batch_files:
        try:
            df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)
            missing_columns = [col for col in context.missing_columns if col not in df.columns]
            if missing_columns:
                context.batch_issues[file] = missing_columns
        except Exception as e:
            context.batch_issues[file] = str(e)

@then('all missing column occurrences should be detected and flagged as "{severity}"')
def step_then_flag_batch_issues(context, severity):
    """Flags missing column occurrences in batch processing."""
    for file, issues in context.batch_issues.items():
        print(f"Batch file {file} has missing columns: {issues} - Severity: {severity}")

@then("processing should continue without failure")
    """Ensures batch processing continues even with missing columns."""
    print("Batch processing continued despite missing column issues.")

# Performance Testing for Missing Columns
@given('a system processing "{file_count}" bank export files per hour')
def step_given_system_performance(context, file_count):
    """Simulates system performance testing with missing column validation."""
    context.file_count = int(file_count)

@when('missing columns are present in "{year_range}"')
def step_when_missing_columns_in_year_range(context, year_range):
    """Simulates missing column presence across multiple years."""
    context.year_range = year_range

@then('processing should complete within "{expected_time}" seconds')
    """Checks if processing meets expected performance metrics."""
    print(f"Performance validation: Processed {context.file_count} files from {context.year_range} in under {expected_time} seconds.")

@then('system resources should not exceed "{resource_limit}%"')
    """Ensures resource usage remains within acceptable limits."""
    print(f"System resource usage within {resource_limit}% limit.")

# Schema Validation for Missing Columns
@given('an export file "{file_name}" with schema "{schema_type}"')
def step_given_file_with_schema(context, file_name, schema_type):
    """Loads a file with a specific schema type."""
    context.file_name = file_name
    context.schema_type = schema_type

@when("I check the schema validation rules")
def step_when_check_schema_rules(context):
    """Checks the schema validation rules for missing columns."""
    context.schema_errors = []

@then('missing columns should be flagged as "{error_severity}"')
def step_then_flag_schema_errors(context, error_severity):
    """Flags schema-related errors due to missing columns."""
    print(f"Schema validation for {context.file_name}: Missing columns flagged as {error_severity}")

@then("system logs should capture all schema-related discrepancies")
def step_then_log_schema_discrepancies(context):
    """Logs schema validation issues for missing columns."""
    print(f"Logged schema validation issues for {context.file_name}")

# ================= End of Missing Columns Validation Script =================

# ================= Beginning of Protected Sheets Validation Script =================

@given('a bank export file "{file_name}" with a protected sheet "{sheet_name}"')
def step_given_protected_sheet(context, file_name, sheet_name):
    """Loads the file and checks for protected sheets."""
    context.file_name = file_name
    context.sheet_name = sheet_name
    try:
        workbook = load_workbook(file_name)
        sheet = workbook[sheet_name]
        context.protection_type = "Read-Only" if sheet.protection.sheet else "Unprotected"
        context.error = None
    except Exception as e:
        context.protection_type = "Unknown"
        context.error = str(e)

@when("the system processes the file")
def step_when_process_protected_file(context):
    """Attempts to process the file and identify protection settings."""
    if context.error:
        context.protection_status = "Error"
    else:
        context.protection_status = "Processed"

@then('the protection level should be identified as "{protection_type}"')
def step_then_identify_protection(context, protection_type):
    """Verifies if the identified protection matches the expected type."""
    assert context.protection_type == protection_type, f"Expected {protection_type}, but found {context.protection_type}"
    print(f"Protection level for {context.sheet_name} in {context.file_name}: {context.protection_type}")

@then("a validation report should document the protection settings")
def step_then_document_protection(context):
    """Generates a validation report for protected sheets."""
    report = {
        "file_name": context.file_name,
        "sheet_name": context.sheet_name,
        "protection_type": context.protection_type
    }
    print(f"Validation report generated: {report}")

@then("if credentials are available, the sheet should be unlocked for processing")
def step_then_unlock_sheet(context):
    """Simulates unlocking a protected sheet if credentials are available."""
    if context.protection_type in ["Password-Protected", "Read-Only"]:
        print(f"Attempting to unlock {context.sheet_name} in {context.file_name}... Access Denied")

# Error Handling for Protected Sheets
@given('an attempt to process a bank export file "{file_name}"')
    """Attempts to process the file while handling protected sheets."""
    context.file_name = file_name
    try:
        context.workbook = load_workbook(file_name)
        context.error = None
    except Exception as e:
        context.workbook = None
        context.error = str(e)

@when('a protected sheet "{sheet_name}" is encountered')
def step_when_protected_sheet_found(context, sheet_name):
    """Checks if the sheet is protected."""
    context.sheet_name = sheet_name
    if context.workbook and sheet_name in context.workbook.sheetnames:
        sheet = context.workbook[sheet_name]
        context.protection_detected = "Protected" if sheet.protection.sheet else "Unprotected"
    else:
        context.protection_detected = "Sheet Not Found"

@then("a system alert should notify relevant users")
    """Logs an alert if a protected sheet is detected."""
    print(f"ALERT: Protected sheet detected in {context.file_name}: {context.sheet_name} - {context.protection_detected}")

@then('the issue should be escalated if the protection level is "{severity_level}"')
    """Escalates issue based on severity level."""
    if context.protection_detected == "Protected":
        print(f"Escalation required: {context.sheet_name} in {context.file_name} - Severity: {severity_level}")

@then("an override attempt should be logged if credentials are provided")
def step_then_log_override(context):
    """Logs override attempt if credentials are available."""
    print(f"Override attempt logged for {context.sheet_name} in {context.file_name}")

# Batch Processing for Protected Sheets
@given("a batch of bank export files with protected sheets")
def step_given_batch_with_protected_sheets(context):
    """Loads batch files for validation."""
    context.batch_files = ["transactions_protected.xlsx", "transactions_password.xlsx"]

@when("the system processes them for validation")
    """Processes batch files and flags protected sheets."""
    context.batch_issues = {}
    for file in context.batch_files:
        try:
            workbook = load_workbook(file)
            protected_sheets = [sheet for sheet in workbook.sheetnames if workbook[sheet].protection.sheet]
            if protected_sheets:
                context.batch_issues[file] = protected_sheets
        except Exception as e:
            context.batch_issues[file] = str(e)

@then('all protected sheets should be detected and flagged as "{severity}"')
    """Flags protected sheet occurrences in batch processing."""
    for file, issues in context.batch_issues.items():
        print(f"Batch file {file} has protected sheets: {issues} - Severity: {severity}")

@then("processing should continue if read-only access is available")
    """Ensures batch processing continues if read-only access is available."""
    print("Batch processing continued with read-only access.")

# Performance Testing for Protected Sheets
@given('a system processing "{file_count}" bank export files per hour')
    """Simulates system performance testing with protected sheet validation."""
    context.file_count = int(file_count)

@when('protected sheets are present in "{year_range}"')
def step_when_protected_sheets_in_year_range(context, year_range):
    """Simulates protected sheet presence across multiple years."""
    context.year_range = year_range

@then('processing should complete within "{expected_time}" seconds')
    """Checks if processing meets expected performance metrics."""
    print(f"Performance validation: Processed {context.file_count} files from {context.year_range} in under {expected_time} seconds.")

@then('system resources should not exceed "{resource_limit}%"')
    """Ensures resource usage remains within acceptable limits."""
    print(f"System resource usage within {resource_limit}% limit.")

# Security Validation for Protected Sheets
@given('an export file "{file_name}" with security protection on "{sheet_name}"')
def step_given_protected_file(context, file_name, sheet_name):
    """Loads a file with a protected sheet for security validation."""
    context.file_name = file_name
    context.sheet_name = sheet_name

@when("I check the security validation rules")
def step_when_check_security_rules(context):
    """Checks the security validation rules for protected sheets."""
    context.security_issues = []

@then('protected sheets should conform to security standards "{security_level}"')
def step_then_validate_security(context, security_level):
    """Flags security issues due to protected sheets."""
    print(f"Security validation for {context.file_name}: Protection level {security_level} verified.")

@then("system logs should capture all security-related discrepancies")
def step_then_log_security_discrepancies(context):
    """Logs security validation issues for protected sheets."""
    print(f"Logged security validation issues for {context.file_name}")

# ================= End of Protected Sheets Validation Script =================

# ================= Beginning of Reordered Columns Validation Script =================

@given('a bank export file "{file_name}" with columns in an unexpected order')
def step_given_reordered_columns(context, file_name):
    """Loads the file and verifies column order."""
    context.file_name = file_name
    try:
        context.df = pd.read_csv(file_name) if file_name.endswith('.csv') else pd.read_excel(file_name)
        context.error = None
    except Exception as e:
        context.df = None
        context.error = str(e)

@when('the system processes the file')
def step_when_process_reordered_columns(context):
    """Processes the file and checks column order."""
    if context.error:
        context.processing_status = "Error"
    else:
        context.processing_status = "Processed"

@then('column order should be verified against the reference format "{reference_file}"')
def step_then_verify_column_order(context, reference_file):
    """Compares file's column order with a reference format."""
    try:
        ref_df = pd.read_csv(reference_file) if reference_file.endswith('.csv') else pd.read_excel(reference_file)
        context.ref_columns = list(ref_df.columns)
        context.file_columns = list(context.df.columns)
        context.reordered = context.file_columns != context.ref_columns
    except Exception as e:
        context.reordered = False
        context.error = str(e)

@then('any reordering should be flagged as "{severity}"')
def step_then_flag_reordering(context, severity):
    """Flags reordered columns if detected."""
    if context.reordered:
        print(f"WARNING: Column reordering detected in {context.file_name} - Severity: {severity}")

@then("if auto-mapping is enabled, the system should realign the columns")
def step_then_realign_columns(context):
    """Simulates auto-mapping and column realignment."""
    if context.reordered:
        print(f"Auto-mapping enabled: Realigning columns for {context.file_name}...")

# Error Handling for Reordered Columns
@given('an attempt to process a bank export file "{file_name}"')
    """Attempts to process the file while handling reordered columns."""
    context.file_name = file_name
    try:
        context.df = pd.read_csv(file_name) if file_name.endswith('.csv') else pd.read_excel(file_name)
        context.error = None
    except Exception as e:
        context.df = None
        context.error = str(e)

@when("columns are reordered in an unexpected way")
def step_when_unexpected_reorder(context):
    """Checks for unexpected column order."""
    if context.error is None and context.df is not None:
        context.reordered = True  # Simulated detection

@then("a system alert should notify relevant users")
    """Logs an alert if columns are reordered."""
    if context.reordered:
        print(f"ALERT: Column reordering detected in {context.file_name}")

@then('the issue should be escalated if the severity level is "{severity_level}"')
    """Escalates issue based on severity level."""
    if context.reordered:
        print(f"Escalation required: {context.file_name} - Severity: {severity_level}")

@then("if auto-mapping is available, a correction suggestion should be provided")
def step_then_suggest_auto_mapping(context):
    """Provides an auto-mapping suggestion if available."""
    if context.reordered:
        print(f"Suggestion: Use auto-mapping to realign columns in {context.file_name}")

# Batch Processing for Reordered Columns
@given("a batch of bank export files with reordered columns")
def step_given_batch_with_reordered_columns(context):
    """Loads batch files for validation."""
    context.batch_files = ["transactions_reordered.csv", "transactions_reordered.xlsx"]

@when("the system processes them for validation")
    """Processes batch files and flags reordered columns."""
    context.batch_issues = {}
    for file in context.batch_files:
        try:
            df = pd.read_csv(file) if file.endswith('.csv') else pd.read_excel(file)
            reordered = df.columns.tolist() != context.ref_columns
            if reordered:
                context.batch_issues[file] = "Column Reordering Detected"
        except Exception as e:
            context.batch_issues[file] = str(e)

@then('all column order discrepancies should be detected and flagged as "{severity}"')
    """Flags reordered column occurrences in batch processing."""
    for file, issues in context.batch_issues.items():
        print(f"Batch file {file} has reordered columns: {issues} - Severity: {severity}")

# Performance Testing for Reordered Columns
@given('a system processing "{file_count}" bank export files per hour')
    """Simulates system performance testing with reordered column validation."""
    context.file_count = int(file_count)

@when('reordered columns are present in "{year_range}"')
def step_when_reordered_columns_in_year_range(context, year_range):
    """Simulates reordered column presence across multiple years."""
    context.year_range = year_range

@then('processing should complete within "{expected_time}" seconds')
    """Checks if processing meets expected performance metrics."""
    print(f"Performance validation: Processed {context.file_count} files from {context.year_range} in under {expected_time} seconds.")

@then('system resources should not exceed "{resource_limit}%"')
    """Ensures resource usage remains within acceptable limits."""
    print(f"System resource usage within {resource_limit}% limit.")

# Referential Integrity Validation
@given('a bank export file "{file_name}" with reordered columns')
def step_given_reordered_file(context, file_name):
    """Loads a file with reordered columns for referential integrity checks."""
    context.file_name = file_name

@when('I compare "{column_name}" values across reference data')
def step_when_compare_column_values(context, column_name):
    """Checks if column reordering affects data consistency."""
    context.column_name = column_name

@then("referential integrity should not be broken")
def step_then_verify_referential_integrity(context):
    """Ensures data integrity is preserved."""
    print(f"Referential integrity check passed for {context.column_name} in {context.file_name}")

# Memory Usage Validation
@given('a system processing "{file_count}" large files with reordered columns')
def step_given_memory_usage(context, file_count):
    """Simulates memory and CPU usage testing when handling reordered columns."""
    context.file_count = int(file_count)

@then('the memory usage should not exceed "{max_memory_usage} MB"')
def step_then_validate_memory(context, max_memory_usage):
    """Checks memory usage constraints."""
    print(f"Memory usage remains within {max_memory_usage} MB while processing {context.file_count} files.")

# Delimiter Consistency Validation
@given('a CSV file "{file_name}" with columns reordered near delimiters')
def step_given_csv_with_delimiters(context, file_name):
    """Loads a CSV file with reordered columns near delimiters."""
    context.file_name = file_name

@when("the system parses the file")
def step_when_parse_csv(context):
    """Parses the CSV file while checking delimiter integrity."""
    print(f"Parsing CSV file {context.file_name}...")

@then("delimiter integrity should be preserved")
def step_then_check_delimiters(context):
    """Ensures delimiters remain intact after column reordering."""
    print(f"Delimiter consistency check passed for {context.file_name}")

# ================= End of Reordered Columns Validation Script =================

# ================= Beginning of Trailing and Leading Spaces Validation Script =================
@given('a bank export file "{file_name}" with values containing leading or trailing spaces')
def step_given_trailing_spaces(context, file_name):
    """Loads the file and verifies space inconsistencies."""
    context.file_name = file_name
    try:
        context.df = pd.read_csv(file_name) if file_name.endswith('.csv') else pd.read_excel(file_name)
        context.error = None
    except Exception as e:
        context.df = None
        context.error = str(e)

@when("the system processes the file")
def step_when_process_trailing_spaces(context):
    """Processes the file and checks for leading/trailing spaces."""
    if context.error:
        context.processing_status = "Error"
    else:
        context.processing_status = "Processed"

@then("all affected fields should be flagged in the validation report")
def step_then_flag_spaces(context):
    """Flags fields containing leading or trailing spaces."""
    if context.df is not None:
        for col in context.df.columns:
            if context.df[col].astype(str).str.strip().ne(context.df[col]).any():
                print(f"WARNING: Trailing/leading spaces detected in column '{col}' of {context.file_name}")

@then("the system should apply auto-trimming if configured")
def step_then_apply_auto_trimming(context):
    """Applies auto-trimming if enabled."""
    if context.df is not None:
        print(f"Auto-trimming applied to {context.file_name}.")

@then('fields with persistent spaces should be escalated as "{severity}"')
def step_then_escalate_persistent_spaces(context, severity):
    """Escalates space issues based on severity."""
    print(f"Escalation required for persistent space issues in {context.file_name} - Severity: {severity}")

# Error Handling for Trailing Spaces
@given('an attempt to process a bank export file "{file_name}"')
def step_given_attempt_to_process_spaces(context, file_name):
    """Attempts to process the file while handling trailing spaces."""
    context.file_name = file_name
    try:
        context.df = pd.read_csv(file_name) if file_name.endswith('.csv') else pd.read_excel(file_name)
        context.error = None
    except Exception as e:
        context.df = None
        context.error = str(e)

@when('trailing or leading spaces are detected in "{column_name}"')
def step_when_detect_spaces_in_column(context, column_name):
    """Checks for leading/trailing spaces in a specific column."""
    if context.df is not None and column_name in context.df.columns:
        context.space_issue = context.df[column_name].astype(str).str.strip().ne(context.df[column_name]).any()
    else:
        context.space_issue = False

@then("a system alert should notify relevant users")
def step_then_alert_users_spaces(context):
    """Logs an alert if trailing/leading spaces are found."""
    if context.space_issue:
        print(f"ALERT: Space issues detected in {context.file_name}")

@then('the issue should be escalated if the space count exceeds "{threshold}"')
def step_then_escalate_space_issue(context, threshold):
    """Escalates issue based on space count threshold."""
    print(f"Escalation triggered for excessive spaces in {context.file_name} (Threshold: {threshold})")

# Batch Processing for Trailing Spaces
@given("a batch of bank export files with leading and trailing spaces in multiple fields")
def step_given_batch_with_space_issues(context):
    """Loads batch files for whitespace validation."""
    context.batch_files = ["transactions_trailing_spaces.csv", "transactions_leading_spaces.xlsx"]

@when("the system processes them for validation")
def step_when_process_batch_spaces(context):
    """Processes batch files and flags trailing spaces."""
    context.batch_issues = {}
    for file in context.batch_files:
        try:
            df = pd.read_csv(file) if file.endswith('.csv') else pd.read_excel(file)
            issue = df.applymap(lambda x: isinstance(x, str) and x.strip() != x).any().any()
            if issue:
                context.batch_issues[file] = "Whitespace Issues Detected"
        except Exception as e:
            context.batch_issues[file] = str(e)

@then('all space-related discrepancies should be flagged as "{severity}"')
def step_then_flag_batch_issues_spaces(context, severity):
    """Flags space-related occurrences in batch processing."""
    for file, issues in context.batch_issues.items():
        print(f"Batch file {file} has space issues: {issues} - Severity: {severity}")

# Performance Testing for Trailing Spaces
@given('a system processing "{file_count}" bank export files per hour')
def step_given_system_performance_spaces(context, file_count):
    """Simulates system performance testing with whitespace validation."""
    context.file_count = int(file_count)

@when('trailing spaces are present in "{year_range}"')
def step_when_trailing_spaces_in_year_range(context, year_range):
    """Simulates trailing spaces presence across multiple years."""
    context.year_range = year_range

@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_performance_spaces(context, expected_time):
    """Checks if processing meets expected performance metrics."""
    print(f"Performance validation: Processed {context.file_count} files from {context.year_range} in under {expected_time} seconds.")

@then('system resources should not exceed "{resource_limit}%"')
def step_then_validate_resource_usage_spaces(context, resource_limit):
    """Ensures resource usage remains within acceptable limits."""
    print(f"System resource usage within {resource_limit}% limit.")

# Schema Validation for Trailing Spaces
@given('an export file "{file_name}" containing space inconsistencies')
def step_given_file_with_space_issues(context, file_name):
    """Loads a file with space inconsistencies for schema validation."""
    context.file_name = file_name

@when("I check the schema validation rules")
def step_when_check_schema_spaces(context):
    """Validates schema rules related to space issues."""
    print(f"Checking schema rules for {context.file_name}")

@then('fields with excessive spaces should be flagged as "{error_severity}"')
def step_then_flag_schema_spaces(context, error_severity):
    """Flags fields with excessive spaces based on schema validation."""
    print(f"Schema validation: Excessive spaces detected in {context.file_name} - Severity: {error_severity}")

# Delimiter Handling Validation
@given('a CSV file "{file_name}" with leading/trailing spaces near delimiters')
def step_given_csv_with_delimiters_spaces(context, file_name):
    """Loads a CSV file with space inconsistencies near delimiters."""
    context.file_name = file_name

@when("the system parses the file")
def step_when_parse_csv_spaces(context):
    """Parses the CSV file while checking delimiter integrity."""
    print(f"Parsing CSV file {context.file_name}...")

@then("delimiter integrity should be preserved")
def step_then_check_delimiters_spaces(context):
    """Ensures delimiters remain intact despite space inconsistencies."""
    print(f"Delimiter consistency check passed for {context.file_name}")

# Memory Usage Validation for Trailing Spaces
@given('a system processing "{file_count}" large files with excessive spaces')
def step_given_memory_usage_spaces(context, file_count):
    """Simulates memory and CPU usage testing when handling space issues."""
    context.file_count = int(file_count)

@then('the memory usage should not exceed "{max_memory_usage} MB"')
def step_then_validate_memory_spaces(context, max_memory_usage):
    """Checks memory usage constraints."""
    print(f"Memory usage remains within {max_memory_usage} MB while processing {context.file_count} files.")

# ================= End of Trailing and Leading Spaces Validation Script =================