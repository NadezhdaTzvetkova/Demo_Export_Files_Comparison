import os
import pandas as pd
import numpy as np

# ✅ Ensure the save directory exists
SAVE_DIR = "test_data/generated_files"
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Define base data
base_data = {
    "Transaction_ID": np.arange(1001, 1021),
    "Amount": np.random.uniform(10, 5000, 20).round(2),
    "Transaction_Date": pd.date_range(start="2022-01-01", periods=20, freq="D"),
    "Customer_Name": ["Alice Johnson", "Mike Brown", "Chris Lee", "Emma Watson"] * 5,
}


# ✅ Function to generate test files
def generate_test_file(file_name, headers):
    """Generate and save a test file ensuring column count matches header count"""
    df = pd.DataFrame(base_data)

    # Adjust DataFrame to match expected headers (fill missing columns with empty values)
    num_headers = len(headers)
    num_columns = len(df.columns)

    if num_headers > num_columns:
        # Add empty columns to match headers
        for i in range(num_headers - num_columns):
            df[f"Extra_Column_{i+1}"] = np.nan

    elif num_headers < num_columns:
        # Trim extra columns
        df = df.iloc[:, :num_headers]

    df.columns = headers  # Apply corrected headers

    file_path = os.path.join(SAVE_DIR, file_name)

    if file_name.endswith(".csv"):
        df.to_csv(file_path, index=False)
    elif file_name.endswith(".xlsx"):
        df.to_excel(file_path, index=False, engine="openpyxl")

    print(f"✅ File {file_name} generated successfully.")


# ✅ Header mismatch scenarios
header_mismatch_scenarios = {
    "transactions_wrong_headers.csv": [
        "Amount",
        "Transaction_ID",
        "Transaction_Date",
        "Customer_Name",
    ],  # Wrong order
    "transactions_missing_headers.xlsx": [
        "Transaction_ID",
        "Transaction_Date",
    ],  # Missing columns
    "transactions_case_mismatch.csv": [
        "transaction_id",
        "amount",
        "transaction_date",
        "customer_name",
    ],  # Wrong case
    "transactions_data_type_mismatch.xlsx": [
        "Transaction_ID",
        "Amount (Text)",
        "Transaction_Date",
        "Customer_Name",
    ],  # Data type issue
}

for file_name, headers in header_mismatch_scenarios.items():
    generate_test_file(file_name, headers)

# ✅ Database consistency validation
database_mismatch_files = {
    "transactions_reordered_headers.csv": [
        "Customer_Name",
        "Transaction_Date",
        "Transaction_ID",
        "Amount",
    ],
    "transactions_duplicate_headers.xlsx": [
        "Transaction_ID",
        "Amount",
        "Amount",
        "Transaction_Date",
    ],
}

for file_name, headers in database_mismatch_files.items():
    generate_test_file(file_name, headers)

# ✅ Batch processing header mismatch
batch_processing_headers = [
    "Transaction_ID",
    "Amount",
    "Transaction_Date",
    "Extra_Header",
]
df_batch = pd.DataFrame(base_data)
df_batch.columns = batch_processing_headers
df_batch.to_csv(os.path.join(SAVE_DIR, "batch_mismatched_headers.csv"), index=False)

# ✅ Error handling for header mismatches
error_handling_files = {
    "transactions_2019.csv": [
        "Unexpected_Header",
        "Transaction_ID",
        "Amount",
        "Transaction_Date",
    ],
    "transactions_2021.xlsx": [
        "Misaligned_Column1",
        "Transaction_ID",
        "Amount",
        "Transaction_Date",
    ],
    "transactions_2023_with_errors.csv": [
        "Transaction_ID",
        "Amount",
        "Transaction_Date",
        "Extra_Header1",
        "Extra_Header2",
    ],
}

for file_name, headers in error_handling_files.items():
    generate_test_file(file_name, headers)

# ✅ Performance testing with header mismatches
performance_headers = [
    "Transaction_ID",
    "Amount",
    "Transaction_Date",
    "Status",
    "Extra_Header",
]
performance_data_1 = {
    "Transaction_ID": np.arange(5001, 5101),
    "Amount": np.random.uniform(10, 5000, 100).round(2),
    "Transaction_Date": pd.date_range(start="2015-01-01", periods=100, freq="D"),
    "Status": ["Completed", "Pending", "Failed", "Completed"] * 25,
    "Extra_Header": ["Performance_Impact"] * 100,
}

performance_data_2 = {
    "Transaction_ID": np.arange(5101, 5601),
    "Amount": np.random.uniform(10, 5000, 500).round(2),
    "Transaction_Date": pd.date_range(start="2021-01-01", periods=500, freq="D"),
    "Status": ["Completed", "Pending", "Failed", "Completed", "Pending"] * 100,
    "Extra_Header": ["Performance_Impact"] * 500,
}

df_performance_1 = pd.DataFrame(performance_data_1)
df_performance_2 = pd.DataFrame(performance_data_2)

df_performance_1.to_csv(
    os.path.join(SAVE_DIR, "performance_2015_2020.csv"), index=False
)

# ✅ Handle missing pyarrow for Parquet
try:
    df_performance_2.to_parquet(
        os.path.join(SAVE_DIR, "performance_2021_2023.parquet"),
        index=False,
        engine="pyarrow",
    )
except ImportError:
    print(
        "⚠️ Warning: pyarrow not installed. Saving performance_2021_2023 as CSV instead."
    )
    df_performance_2.to_csv(
        os.path.join(SAVE_DIR, "performance_2021_2023.csv"), index=False
    )

print("\n🎉 All header mismatch test files generated successfully!")
