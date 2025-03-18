import os
import pandas as pd
import numpy as np

# ✅ Ensure save directory exists
SAVE_DIR = "test_data/generated_files"
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Base dataset (complete set of columns)
base_columns = ["Transaction ID", "Amount", "Transaction Date", "Account Number", "Currency Code"]
base_data = {
    "Transaction ID": np.arange(1001, 1021),
    "Amount": np.random.uniform(10, 5000, 20).round(2),
    "Transaction Date": pd.date_range(start="2022-01-01", periods=20, freq="D"),
    "Account Number": [f"ACC{np.random.randint(100, 999)}" for _ in range(20)],
    "Currency Code": ["USD", "EUR", "GBP", "JPY"] * 5,
}

# ✅ Function to generate test files with missing columns
def generate_missing_column_file(file_name, missing_columns):
    """Generate a file with specific missing columns."""
    df = pd.DataFrame(base_data)

    # Remove specified missing columns
    for col in missing_columns:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    file_path = os.path.join(SAVE_DIR, file_name)

    if file_name.endswith(".csv"):
        df.to_csv(file_path, index=False)
    elif file_name.endswith(".xlsx"):
        df.to_excel(file_path, index=False, engine="openpyxl")

    print(f"✅ File {file_name} generated successfully with missing columns: {missing_columns}")

# ✅ Generate missing column test files
missing_column_files = {
    "transactions_missing_account.csv": ["Account Number"],
    "transactions_missing_currency.xlsx": ["Currency Code"],
    "transactions_partial_missing.csv": ["Date", "Transaction ID"],
}

for file_name, missing_cols in missing_column_files.items():
    generate_missing_column_file(file_name, missing_cols)

# ✅ Error handling test cases for missing columns
error_handling_files = {
    "transactions_2019.csv": ["Transaction ID"],
    "transactions_2021.xlsx": ["Amount"],
    "transactions_with_gaps.xlsx": ["Date", "Account Number"],
}

for file_name, missing_cols in error_handling_files.items():
    generate_missing_column_file(file_name, missing_cols)

# ✅ Batch processing test cases
batch_processing_files = ["batch_high.csv", "batch_medium.csv", "batch_low.csv"]

for file_name in batch_processing_files:
    generate_missing_column_file(file_name, ["Amount"])  # Example missing column

# ✅ Performance testing (simulate large datasets)
def create_large_csv(file_name, row_count, missing_columns):
    """Generate a large CSV file with missing columns for performance testing."""
    df = pd.DataFrame(base_data).iloc[:row_count]

    # Remove specified missing columns
    for col in missing_columns:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    file_path = os.path.join(SAVE_DIR, file_name)
    df.to_csv(file_path, index=False)
    print(f"✅ Large file {file_name} generated successfully.")

# ✅ Create performance test files
create_large_csv("performance_2015_2020.csv", 100, ["Currency Code"])
create_large_csv("performance_2021_2023.csv", 500, ["Account Number"])

# ✅ Schema validation test cases
schema_validation_files = {
    "transactions_legacy.csv": ["Transaction Date"],
    "transactions_modified.xlsx": ["Amount"],
    "transactions_test.csv": ["Account Number"],
}

for file_name, missing_cols in schema_validation_files.items():
    generate_missing_column_file(file_name, missing_cols)

print("\n🎉 All missing column validation test files generated successfully!")
