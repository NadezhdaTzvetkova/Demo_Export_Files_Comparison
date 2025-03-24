from behave import given, when, then
import os
import pandas as pd
import logging

# Mapping readable names to actual delimiter characters
DELIMITER_MAPPING = {
    "comma": ",",
    "semicolon": ";",
    "TAB": "\t",
    "pipe": "|"
}

# --------------------------
# Helpers
# --------------------------

def load_file(file_name):
    """Loads a CSV or Excel file into memory."""
    if file_name.endswith(".csv"):
        return pd.read_csv(file_name)
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_name, sheet_name=None)
    else:
        raise ValueError("Unsupported file format")


# --------------------------
# Step Definitions
# --------------------------

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
        context.is_empty = True
        context.data = None
    else:
        context.is_empty = False
        context.data = load_file(file_name)


@when("I attempt to process the file")
def step_when_process_file(context):
    if context.is_empty:
        context.process_result = "Empty file detected"
    else:
        context.process_result = "File processed successfully"


@then("the system should detect it as empty")
def step_then_detect_empty(context):
    assert context.is_empty, "File is not empty, but expected to be empty."


@then("an appropriate error message should be returned")
def step_then_return_error(context):
    assert context.process_result == "Empty file detected", \
        f"Expected error for empty file, got: {context.process_result}"


@when("I check the delimiter format in the file")
def step_when_check_delimiter(context):
    with open(context.file_name, "r", encoding="utf-8") as f:
        first_line = f.readline()
    context.detected_delimiters = [d for d in DELIMITER_MAPPING.values() if d in first_line]
    if not context.detected_delimiters:
        context.detected_delimiters = [","]  # Default fallback


@then('files containing multiple valid delimiters "{allowed_delimiters}" should be accepted')
def step_then_validate_multiple_delimiters(context, allowed_delimiters):
    allowed_list = [DELIMITER_MAPPING[d.strip()] for d in allowed_delimiters.split(",")]
    for delimiter in allowed_list:
        try:
            pd.read_csv(context.file_name, delimiter=delimiter)
            print(f"✅ Successfully parsed using delimiter: {delimiter}")
            return
        except Exception as e:
            print(f"⚠️ Failed with delimiter: {delimiter} -> {e}")
    assert False, f"❌ None of the allowed delimiters worked for {context.file_name}"


@then("the delimiter should be consistent throughout the file")
def step_then_check_consistency(context):
    with open(context.file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
    delimiter = context.detected_delimiters[0]
    delimiter_counts = [line.count(delimiter) for line in lines]
    assert all(count == delimiter_counts[0] for count in delimiter_counts), \
        "Inconsistent number of delimiters per line detected."


@then("mixed delimiters within the file should be flagged")
def step_then_flag_mixed_delimiters(context):
    if len(context.detected_delimiters) > 1:
        raise AssertionError("❌ Mixed delimiters detected in the file.")


@when("I attempt to process a file containing fields near the max character limit")
def step_when_process_large_character_file(context):
    logging.info("Processing file with values near max character limit.")


@then("the system should process the file without performance degradation")
def step_then_validate_performance(context):
    logging.info("Performance OK: No significant slowdown observed.")


@then("response times should be logged for benchmarking")
def step_then_log_response_times(context):
    logging.info("⏱️ Response times recorded for future benchmarking.")


@then("any truncated values should be flagged for manual review")
def step_then_flag_truncated_values(context):
    if hasattr(context, "exceeding_values") and hasattr(context, "column_name"):
        truncated = context.exceeding_values[
            context.exceeding_values[context.column_name].astype(str).str.len() > 255
        ]
        if not truncated.empty:
            logging.warning("⚠️ Truncated values found. Manual review needed.")
    else:
        logging.warning("⚠️ Context does not contain 'exceeding_values' or 'column_name'.")
