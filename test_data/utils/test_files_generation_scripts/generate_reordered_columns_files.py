import os
import pandas as pd
import numpy as np

# ✅ Ensure save directory exists
SAVE_DIR = "test_data/generated_files"
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Standard column order (reference structure)
STANDARD_COLUMNS = [
    "Transaction ID",
    "Account Number",
    "Amount",
    "Transaction Date",
    "Currency Code",
]


# ✅ Function to create a CSV file with reordered columns
def create_reordered_csv(file_name, severity, reorder_columns=None):
    """Generate a CSV file with specified column order."""
    data = {
        "Transaction ID": np.arange(1001, 1011),
        "Account Number": [f"ACC{i}" for i in range(101, 111)],
        "Amount": np.random.uniform(10, 5000, 10),
        "Transaction Date": pd.date_range(
            start="2024-01-01", periods=10, freq="D"
        ).strftime("%Y-%m-%d"),
        "Currency Code": ["USD"] * 10,
    }

    df = pd.DataFrame(data)

    # If column reordering is needed
    if reorder_columns:
        df = df[reorder_columns]

    # Save the CSV file
    file_path = os.path.join(SAVE_DIR, file_name)
    df.to_csv(file_path, index=False)
    print(f"✅ File {file_name} generated successfully with {severity} severity.")


# ✅ Function to create an Excel file with reordered columns
def create_reordered_excel(file_name, severity, reorder_columns=None):
    """Generate an Excel file with specified column order."""
    data = {
        "Transaction ID": np.arange(1001, 1011),
        "Account Number": [f"ACC{i}" for i in range(101, 111)],
        "Amount": np.random.uniform(10, 5000, 10),
        "Transaction Date": pd.date_range(
            start="2024-01-01", periods=10, freq="D"
        ).strftime("%Y-%m-%d"),
        "Currency Code": ["USD"] * 10,
    }

    df = pd.DataFrame(data)

    # If column reordering is needed
    if reorder_columns:
        df = df[reorder_columns]

    # Save the Excel file
    file_path = os.path.join(SAVE_DIR, file_name)
    df.to_excel(file_path, index=False, engine="openpyxl")
    print(f"✅ File {file_name} generated successfully with {severity} severity.")


# ✅ Generate test files for reordered columns
reordered_files = {
    "transactions_reordered.csv": ("transactions_standard.csv", "High"),
    "transactions_reordered.xlsx": ("transactions_standard.xlsx", "Medium"),
    "transactions_partial_reorder.xlsx": ("transactions_standard_partial.xlsx", "Low"),
}

for file_name, (reference_file, severity) in reordered_files.items():
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    if file_name.endswith(".csv"):
        create_reordered_csv(file_name, severity, reordered_columns)
    else:
        create_reordered_excel(file_name, severity, reordered_columns)

# ✅ Generate error handling test cases for reordered columns
error_handling_files = {
    "transactions_2020_reordered.csv": "High",
    "transactions_2021_reordered.xlsx": "Medium",
    "transactions_test_reorder.xlsx": "Low",
}

for file_name, severity in error_handling_files.items():
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    if file_name.endswith(".csv"):
        create_reordered_csv(file_name, severity, reordered_columns)
    else:
        create_reordered_excel(file_name, severity, reordered_columns)

# ✅ Generate batch processing test cases
batch_processing_files = [
    "batch_high_reorder.csv",
    "batch_medium_reorder.xlsx",
    "batch_low_reorder.csv",
]

for file_name in batch_processing_files:
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    if file_name.endswith(".csv"):
        create_reordered_csv(file_name, "Batch Processing", reordered_columns)
    else:
        create_reordered_excel(file_name, "Batch Processing", reordered_columns)


# ✅ Generate performance testing files (simulate large dataset)
def create_large_reordered_file(file_name, row_count, severity):
    """Generate a large dataset for performance testing."""
    data = {
        "Transaction ID": np.arange(1, row_count + 1),
        "Account Number": [f"ACC{i}" for i in range(1, row_count + 1)],
        "Amount": np.random.uniform(10, 5000, row_count),
        "Transaction Date": pd.date_range(
            start="2024-01-01", periods=row_count, freq="D"
        ).strftime("%Y-%m-%d"),
        "Currency Code": ["USD"] * row_count,
    }

    df = pd.DataFrame(data)
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    df = df[reordered_columns]

    file_path = os.path.join(SAVE_DIR, file_name)
    if file_name.endswith(".csv"):
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False, engine="openpyxl")

    print(f"✅ Large file {file_name} generated successfully with {severity} severity.")


# ✅ Create performance test files
create_large_reordered_file("performance_2015_2020.csv", 100, "High")
create_large_reordered_file("performance_2021_2023.xlsx", 500, "Medium")

# ✅ Generate referential integrity test cases
referential_integrity_files = {
    "transactions_reordered.csv": ("Account Number", "High"),
    "transactions_partial_reorder.xlsx": ("Transaction ID", "Medium"),
}

for file_name, (column_name, severity) in referential_integrity_files.items():
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    if file_name.endswith(".csv"):
        create_reordered_csv(file_name, severity, reordered_columns)
    else:
        create_reordered_excel(file_name, severity, reordered_columns)

# ✅ Generate auto-mapping test cases
auto_mapping_files = {
    "transactions_reordered.csv": ("transactions_standard.csv", "High"),
    "transactions_reordered.xlsx": ("transactions_standard.xlsx", "Medium"),
}

for file_name, (reference_file, severity) in auto_mapping_files.items():
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    if file_name.endswith(".csv"):
        create_reordered_csv(file_name, severity, reordered_columns)
    else:
        create_reordered_excel(file_name, severity, reordered_columns)

# ✅ Generate memory usage validation test cases
memory_usage_files = {
    "transactions_reordered_large_500.csv": (500, "High"),
    "transactions_reordered_large_1000.xlsx": (1000, "Medium"),
}

for file_name, (row_count, severity) in memory_usage_files.items():
    create_large_reordered_file(file_name, row_count, severity)

# ✅ Generate delimiter consistency test cases
delimiter_files = [
    "transactions_reordered_delimiters.csv",
    "transactions_misaligned_delim.csv",
]

for file_name in delimiter_files:
    reordered_columns = np.random.permutation(STANDARD_COLUMNS).tolist()
    create_reordered_csv(file_name, "Delimiter Consistency", reordered_columns)

print("\n🎉 All reordered column validation test files generated successfully!")
