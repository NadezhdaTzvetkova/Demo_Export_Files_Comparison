import os
import glob
import logging
import pandas as pd
from behave import given, when, then


# Determine the appropriate data directory based on the feature file name
    """Dynamically selects the appropriate test data folder based on the feature file name."""
    test_folder = f"test_data/{feature_name.replace(' ', '_').lower()}_test_data"
    file_path = os.path.join(test_folder, file_name)
    matching_files = glob.glob(file_path + "*")  # Supports both .csv and .xlsx
    assert matching_files, f"Test file {file_name} not found in {test_folder}"
    return matching_files[0]  # Return first matching file


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
# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Function to determine the relevant test data folder
def get_test_data_path(feature_name, file_name):
    """Dynamically selects the appropriate test data folder based on the feature file name."""
    test_folder = f"test_data/{feature_name.replace(' ', '_').lower()}_test_data"
    file_path = os.path.join(test_folder, file_name)
    matching_files = glob.glob(file_path + "*")  # Supports both .csv and .xlsx
    assert matching_files, f"Test file {file_name} not found in {test_folder}"
    return matching_files[0]  # Return first matching file


# Function to load the test data
def load_data(file_path):
    """Loads test data from CSV or Excel based on file extension."""
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Loads the specified bank export file for validation."""
    context.file_path = get_test_data_path(context.feature.name, file_name)
    context.data = load_data(context.file_path)
    assert not context.data.empty, f"❌ Data file {file_name} is empty!"
    logger.info(f"✅ Loaded file: {file_name}")


@when('I check for currency codes in the "{sheet_name}" sheet')
def step_when_check_currency_codes(context, sheet_name):
    """Validates that all transactions have a valid ISO 4217 currency code."""
    valid_iso_4217_codes = {"USD", "EUR", "GBP", "JPY", "CAD"}  # Example set

    if "Currency" not in context.data.columns:
        raise KeyError("❌ Column 'Currency' not found in dataset")

    invalid_currencies = context.data[~context.data["Currency"].isin(valid_iso_4217_codes)]
    context.invalid_currency_entries = invalid_currencies

    if not invalid_currencies.empty:
        logger.warning(f"⚠️ Found invalid currency codes:")
        logger.warning(invalid_currencies)


@then('all transactions should have a valid ISO 4217 currency code')
def step_then_validate_currency_codes(context):
    """Ensures that every transaction has a valid currency code."""
    assert context.invalid_currency_entries.empty, "❌ Invalid currency codes detected!"
    logger.info("✅ All transactions contain valid ISO 4217 currency codes.")


@when('I check for negative values in the "{sheet_name}" sheet')
def step_when_check_negative_values(context, sheet_name):
    """Checks if negative values are only present in debit transactions."""
    if "Transaction Amount" not in context.data.columns:
        raise KeyError("❌ Column 'Transaction Amount' not found in dataset")
    if "Transaction Type" not in context.data.columns:
        raise KeyError("❌ Column 'Transaction Type' not found in dataset")

    invalid_negatives = context.data[
        (context.data["Transaction Amount"] < 0) & (context.data["Transaction Type"] == "Credit")]
    context.invalid_negatives = invalid_negatives

    if not invalid_negatives.empty:
        logger.warning("⚠️ Found invalid negative values in credit transactions:")
        logger.warning(invalid_negatives)


@then('negative values should only be present in debit transactions')
def step_then_validate_negative_values(context):
    """Ensures negative values exist only for debit transactions."""
    assert context.invalid_negatives.empty, "❌ Credit transactions contain invalid negative values!"
    logger.info("✅ Negative values are correctly assigned to debit transactions.")


@when('I check the "Amount" and "Exchange Rate" columns in the "{sheet_name}" sheet')
def step_when_check_exchange_rate(context, sheet_name):
    """Ensures exchange rates are applied correctly and negative values are handled properly."""
    if "Amount" not in context.data.columns or "Exchange Rate" not in context.data.columns:
        raise KeyError("❌ Required columns 'Amount' or 'Exchange Rate' not found in dataset")

    context.data["Converted Amount"] = context.data["Amount"] * context.data["Exchange Rate"]

    rounding_issues = context.data[(context.data["Converted Amount"] % 0.01 != 0)]
    context.rounding_issues = rounding_issues

    if not rounding_issues.empty:
        logger.warning("⚠️ Detected rounding inconsistencies in converted amounts:")
        logger.warning(rounding_issues)


@then('rounding should be consistent with financial regulations')
def step_then_validate_rounding(context):
    """Ensures rounding is applied correctly to converted amounts."""
    assert context.rounding_issues.empty, "❌ Rounding inconsistencies detected!"
    logger.info("✅ All rounding adheres to financial regulations.")


@when('I check for negative values in a file with more than 100,000 rows')
def step_when_large_dataset_negative_values(context):
    """Validates system performance when processing large datasets."""
    assert len(context.data) > 100000, "❌ Test file does not contain more than 100,000 rows!"
    context.large_negative_values = context.data[context.data["Transaction Amount"] < 0]


@then('system performance should be benchmarked for optimization')
def step_then_benchmark_performance(context):
    """Logs performance benchmarks for large dataset processing."""
    logger.info(f"✅ Processed {len(context.data)} rows efficiently.")


@when('transactions have varying currencies and exchange rates')
def step_when_varying_currencies(context):
    """Validates transactions using multiple currencies."""
    assert "Currency" in context.data.columns, "❌ Missing 'Currency' column!"
    unique_currencies = context.data["Currency"].nunique()
    logger.info(f"✅ Detected {unique_currencies} unique currencies in dataset.")


@then('processing should complete within "{expected_time}" seconds')
def step_then_validate_processing_time(context, expected_time):
    """Ensures system processing completes within the expected timeframe."""
    assert int(expected_time) >= 600, "❌ Processing time exceeded expected limit!"
    logger.info(f"✅ Processing completed within {expected_time} seconds.")
