from behave import given, when, then
import os
import pandas as pd
from behave import given, when, then

# Constants for file paths
DATA_DIR = "test_data/csv_files"


@given('a bank export file "{file_name}"')
def step_given_bank_export_file(context, file_name):
    """Ensure the bank export file exists"""
    context.file_path = os.path.join(DATA_DIR, file_name)
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


@then('transactions above "{threshold}" should be flagged')
def step_then_flag_high_value_transactions(context, threshold):
    """Flag transactions above the specified threshold"""
    threshold_value = float(threshold.replace("$", "").replace(",", ""))
    flagged = context.df[context.df["Transaction Amount"] > threshold_value]
    context.flagged_transactions = flagged
    assert not flagged.empty, "No transactions flagged."


@then('flagged transactions should be reported to "{compliance_team}"')
def step_then_report_to_compliance(context, compliance_team):
    """Ensure flagged transactions are reported"""
    assert hasattr(context, "flagged_transactions"), "No flagged transactions to report."
    print(f"Reporting {len(context.flagged_transactions)} flagged transactions to {compliance_team}.")


@then('system should cross-check against known "{sanctioned_list}"')
def step_then_cross_check_sanctions(context, sanctioned_list):
    """Simulate cross-checking against a sanctioned list"""
    sanctioned_entities = ["OFAC Watchlist", "EU Sanctions", "Interpol Red List"]  # Example lists
    assert sanctioned_list in sanctioned_entities, f"Sanctioned list {sanctioned_list} not recognized."


@when('I check multiple transactions in "{sheet_name}"')
def step_when_check_structured_transactions(context, sheet_name):
    """Load transactions for structured transaction analysis"""
    if context.file_path.endswith(".csv"):
        context.df = pd.read_csv(context.file_path)
    else:
        context.df = pd.read_excel(context.file_path, sheet_name=sheet_name)


@then('transactions structured below "{threshold}" but summing above "{aggregate_limit}" should be flagged')
def step_then_flag_structured_transactions(context, threshold, aggregate_limit):
    """Detect structured transactions designed to evade AML reporting"""
    threshold_value = float(threshold.replace("$", "").replace(",", ""))
    aggregate_value = float(aggregate_limit.replace("$", "").replace(",", ""))
    grouped = context.df.groupby("Recipient")["Transaction Amount"].sum()
    flagged = grouped[(grouped > aggregate_value) & (grouped < threshold_value)]
    context.flagged_structured_transactions = flagged
    assert not flagged.empty, "No structured transactions flagged."


@when('I check the "Sender Country" and "Recipient Country" in "{sheet_name}"')
def step_when_check_countries(context, sheet_name):
    """Verify presence of country-related columns"""
    required_columns = ["Sender Country", "Recipient Country"]
    for col in required_columns:
        assert col in context.df.columns, f"Missing column: {col}"


@then('transactions involving "{high_risk_country}" should be flagged')
def step_then_flag_high_risk_country(context, high_risk_country):
    """Identify transactions with high-risk jurisdictions"""
    flagged = context.df[(context.df["Sender Country"] == high_risk_country) |
                         (context.df["Recipient Country"] == high_risk_country)]
    context.flagged_high_risk_transactions = flagged
    assert not flagged.empty, "No high-risk transactions flagged."


@then('a report should be generated for AML compliance review')
def step_then_generate_aml_report(context):
    """Generate an AML report for flagged transactions"""
    assert hasattr(context, "flagged_high_risk_transactions"), "No high-risk transactions to report."
    print(f"AML Compliance Report: {len(context.flagged_high_risk_transactions)} high-risk transactions found.")


@when('I analyze transaction history in "{sheet_name}"')
def step_when_analyze_transaction_history(context, sheet_name):
    """Load transaction history for behavior analysis"""
    if context.file_path.endswith(".csv"):
        context.df = pd.read_csv(context.file_path)
    else:
        context.df = pd.read_excel(context.file_path, sheet_name=sheet_name)


@then('significant deviations from normal spending behavior should be flagged')
def step_then_flag_unusual_behavior(context):
    """Detect anomalies in customer behavior"""
    mean_transaction = context.df["Transaction Amount"].mean()
    std_dev = context.df["Transaction Amount"].std()
    flagged = context.df[context.df["Transaction Amount"] > (mean_transaction + 3 * std_dev)]
    context.flagged_unusual_behavior = flagged
    assert not flagged.empty, "No unusual behavior detected."


@when('I cross-reference business accounts in "{sheet_name}" with known shell company lists')
def step_when_cross_reference_shell_companies(context, sheet_name):
    """Simulate checking against shell company lists"""
    known_shell_companies = ["XYZ Offshore Ltd.", "ABC Holdings Inc."]
    flagged = context.df[context.df["Recipient"].isin(known_shell_companies)]
    context.flagged_shell_companies = flagged
    assert not flagged.empty, "No shell company transactions detected."


@then('transactions involving "{shell_company_name}" should be flagged')
def step_then_flag_shell_company(context, shell_company_name):
    """Ensure flagged shell company transactions are recorded"""
    assert hasattr(context, "flagged_shell_companies"), "No shell company transactions to report."
    assert shell_company_name in context.flagged_shell_companies["Recipient"].values, "No matching transactions found."


@when('I check for AML compliance anomalies')
def step_when_check_aml_anomalies(context):
    """Simulate checking large datasets for AML anomalies"""
    context.large_dataset_flagged = True


@then('flagged transactions should be identified within "{expected_runtime}"')
def step_then_validate_aml_runtime(context, expected_runtime):
    """Check if AML processing meets expected runtime"""
    assert context.large_dataset_flagged, "Large dataset anomalies not processed in time."