import os
import sys
import subprocess


def get_project_root():
    """Return the root directory of the project."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def run_command(command):
    """Run a shell command and check for errors."""
    print(f"🛠️ Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=get_project_root())

    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        print(f"Error output:\n{result.stderr}")
        sys.exit(result.returncode)
    else:
        print(f"✅ Command succeeded: {command}")
        print(f"Output:\n{result.stdout}")


# Define available test suites based on provided tags
TEST_SUITES = {
    "all": "",
    "export_comparison": "--tags=export_comparison",
    "data_validation": "--tags=data_validation",
    "currency": "--tags=currency",
    "currency_match": "--tags=currency_match",
    "date_format": "--tags=date_format",
    "date_format_check": "--tags=date_format_check",
    "decimal_precision": "--tags=decimal_precision",
    "decimal_precision_check": "--tags=decimal_precision_check",
    "delimiter_issues": "--tags=delimiter_issues",
    "delimiter_check": "--tags=delimiter_check",
    "encoding": "--tags=encoding",
    "encoding_match": "--tags=encoding_match",
    "account_numbers": "--tags=account_numbers",
    "account_number_format": "--tags=account_number_format",
    "invalid_currency_check": "--tags=invalid_currency_check",
    "missing_values": "--tags=missing_values",
    "missing_values_check": "--tags=missing_values_check",
    "negative_values": "--tags=negative_values",
    "negative_values_check": "--tags=negative_values_check",
    "special_characters": "--tags=special_characters",
    "special_character_check": "--tags=special_character_check",
    "whitespace": "--tags=whitespace",
    "whitespace_check": "--tags=whitespace_check",
    "duplicate_tests": "--tags=duplicate_tests",
    "data_integrity": "--tags=data_integrity",
    "duplicate_account_check": "--tags=duplicate_account_check",
    "customer_duplicates": "--tags=customer_duplicates",
    "duplicate_customer_check": "--tags=duplicate_customer_check",
    "duplicate_check": "--tags=duplicate_check",
    "fraud_detection": "--tags=fraud_detection",
    "fraudulent_transaction_check": "--tags=fraudulent_transaction_check",
    "orphaned_transactions": "--tags=orphaned_transactions",
    "orphaned_transaction_check": "--tags=orphaned_transaction_check",
    "transaction_mismatch": "--tags=transaction_mismatch",
    "transaction_mismatch_check": "--tags=transaction_mismatch_check",
    "edge_cases": "--tags=edge_cases",
    "edge_cases_check": "--tags=edge_cases_check",
    "empty_files": "--tags=empty_files",
    "empty_file_check": "--tags=empty_file_check",
    "hidden_rows": "--tags=hidden_rows",
    "hidden_rows_check": "--tags=hidden_rows_check",
    "character_limit": "--tags=character_limit",
    "max_character_check": "--tags=max_character_check",
    "null_values": "--tags=null_values",
    "null_values_check": "--tags=null_values_check",
    "outliers": "--tags=outliers",
    "outlier_detection": "--tags=outlier_detection",
    "zero_transactions": "--tags=zero_transactions",
    "zero_value_transaction_check": "--tags=zero_value_transaction_check",
    "performance_tests": "--tags=performance_tests",
    "concurrent_processing": "--tags=concurrent_processing",
    "processing_delay": "--tags=processing_delay",
    "processing_time_check": "--tags=processing_time_check",
    "high_concurrency": "--tags=high_concurrency",
    "high_concurrency_check": "--tags=high_concurrency_check",
    "large_dataset": "--tags=large_dataset",
    "large_data_processing": "--tags=large_data_processing",
    "large_transactions": "--tags=large_transactions",
    "large_transactions_test": "--tags=large_transactions_test",
    "memory_usage": "--tags=memory_usage",
    "memory_efficiency_check": "--tags=memory_efficiency_check",
    "regression_tests": "--tags=regression_tests",
    "duplicate_imports": "--tags=duplicate_imports",
    "duplicate_imports_check": "--tags=duplicate_imports_check",
    "historical_data": "--tags=historical_data",
    "bug_fix_verification": "--tags=bug_fix_verification",
    "regression_high_volume": "--tags=regression_high_volume",
    "previous_bugs": "--tags=previous_bugs",
    "transaction_reference_uniqueness": "--tags=transaction_reference_uniqueness",
    "unique_transaction_references": "--tags=unique_transaction_references",
    "structural_tests": "--tags=structural_tests",
    "case_sensitivity": "--tags=case_sensitivity",
    "column_case_insensitivity": "--tags=column_case_insensitivity",
    "column_format": "--tags=column_format",
    "column_format_check": "--tags=column_format_check",
    "extra_columns": "--tags=extra_columns",
    "extra_columns_check": "--tags=extra_columns_check",
    "header_mismatch": "--tags=header_mismatch",
    "header_mismatch_check": "--tags=header_mismatch_check",
    "merged_cells": "--tags=merged_cells",
    "merged_cells_check": "--tags=merged_cells_check",
    "missing_columns": "--tags=missing_columns",
    "missing_columns_check": "--tags=missing_columns_check",
    "protected_sheets": "--tags=protected_sheets",
    "protected_sheet_check": "--tags=protected_sheet_check",
    "column_order": "--tags=column_order",
    "column_order_check": "--tags=column_order_check",
    "trailing_spaces": "--tags=trailing_spaces",
    "trailing_spaces_check": "--tags=trailing_spaces_check"
}


def run_tests(suite):
    """Runs the specified test suite with Allure reporting."""
    if suite not in TEST_SUITES:
        print(f"❌ Invalid suite '{suite}'. Choose from: {list(TEST_SUITES.keys())}")
        sys.exit(1)

    print(f"🚀 Running test suite: {suite}")

    # Run Behave with the selected suite
    behave_cmd = f"behave {TEST_SUITES[suite]} --format=allure_behave.formatter:AllureFormatter -o reports/allure_results"
    run_command(behave_cmd)

    print("📊 Generating Allure report...")
    run_command("allure generate reports/allure_results -o reports/allure_report --clean")

    print("✅ Test execution completed! To view the report, run:")
    print("🔍 allure open reports/allure_report")


if __name__ == "__main__":
    print("📦 Installing dependencies...")
    run_command("python utils/install_dependencies.py")

    if len(sys.argv) < 2:
        print("⚠️ Usage: python run_tests.py <suite>")
        print(f"Available suites: {list(TEST_SUITES.keys())}")
        sys.exit(1)

    suite_name = sys.argv[1]
    run_tests(suite_name)
