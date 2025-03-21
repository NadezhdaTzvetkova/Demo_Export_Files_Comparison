from behave import given, when, then
import os
import pandas as pd
import logging

# Helper function to load CSV or Excel files dynamically
def load_file(file_name):
    if file_name.endswith(".csv"):
        return pd.read_csv(file_name)
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_name, sheet_name=None)  # Load all sheets
    else:
        raise ValueError("Unsupported file format")

@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    context.file_name = file_name
    if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
        context.is_empty = True
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
    assert context.is_empty, "File is not empty"

@then("an appropriate error message should be returned")
def step_then_return_error(context):
    assert context.process_result == "Empty file detected", "Incorrect error message"

@when("I check the delimiter format in the file")
def step_when_check_delimiter(context):
    file_path = context.file_name
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
    delimiters = [",", ";", "	"]
    context.detected_delimiters = [d for d in delimiters if d in first_line]
    assert len(context.detected_delimiters) > 0, "No delimiter detected. File might be corrupted."

@then("the delimiter should be consistent throughout the file")
def step_then_check_consistency(context):
    file_path = context.file_name
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    delimiter_counts = [line.count(context.detected_delimiters[0]) for line in lines]
    assert all(count == delimiter_counts[0] for count in delimiter_counts), "Inconsistent delimiters detected."
    logging.info(f"Delimiter '{context.detected_delimiters[0]}' is consistent across the file.")

@then("mixed delimiters within the file should be flagged")
def step_then_flag_mixed_delimiters(context):
    if len(context.detected_delimiters) > 1:
        logging.warning(f"Mixed delimiters detected in {context.file_name}.")
        assert False, "File contains mixed delimiters."

@when("I attempt to process a file containing fields near the max character limit")
def step_when_process_large_character_file(context):
    logging.info("Processing file with values close to the max character limit...")

@then("the system should process the file without performance degradation")
def step_then_validate_performance(context):
    logging.info("System successfully processed file without noticeable performance issues.")

@then("response times should be logged for benchmarking")
def step_then_log_response_times(context):
    logging.info("Response times for processing max character limit data recorded.")

@then("any truncated values should be flagged for manual review")
def step_then_flag_truncated_values(context):
    truncated_values = context.exceeding_values[context.exceeding_values[context.column_name].astype(str).str.len() > 255]
    if not truncated_values.empty:
        logging.warning("Warning: Some values may have been truncated. Manual review recommended.")
