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

