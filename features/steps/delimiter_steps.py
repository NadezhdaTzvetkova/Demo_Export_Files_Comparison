import os
import pandas as pd
from behave import given, when, then

# Map human-readable delimiter names to actual characters
DELIMITER_MAPPING = {
    "comma": ",",
    "semicolon": ";",
    "TAB": "\t",
    "pipe": "|"
}


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

# Additional test steps for different delimiter validations...

# ================= End of Delimiter Inconsistency Validation =================
