import os
import pandas as pd
import numpy as np

# ✅ Ensure save directory exists
SAVE_DIR = "test_data/generated_files"
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Standard column structure
STANDARD_COLUMNS = ["Transaction ID", "Account Number", "Amount", "Transaction Date", "Currency Code"]

# ✅ Function to create CSV file with trailing/leading spaces
def create_csv_with_spaces(file_name, severity, space_type="trailing"):
    """Generate a CSV file with values containing leading or trailing spaces."""
    data = {
        "Transaction ID": np.arange(1001, 1011),
        "Account Number": [f"ACC{i}" for i in range(101, 111)],
        "Amount": np.random.uniform(10, 5000, 10),
        "Transaction Date": pd.date_range(start="2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d"),
        "Currency Code": ["USD" for _ in range(10)],
    }

    df = pd.DataFrame(data)

    # Apply trailing or leading spaces based on type
    if space_type == "leading":
        df = df.astype(str).apply(lambda x: x.map(lambda v: f"  {v}"))
    elif space_type == "trailing":
        df = df.astype(str).apply(lambda x: x.map(lambda v: f"{v}  "))
    elif space_type == "mixed":
        df = df.astype(str).apply(lambda x: x.map(lambda v: f"  {v}  "))

    file_path = os.path.join(SAVE_DIR, file_name)
    df.to_csv(file_path, index=False)
    print(f"✅ File {file_name} generated successfully with {severity} severity.")

# ✅ Function to create Excel file with trailing/leading spaces
def create_excel_with_spaces(file_name, severity, space_type="trailing"):
    """Generate an Excel file with values containing leading or trailing spaces."""
    data = {
        "Transaction ID": np.arange(1001, 1011),
        "Account Number": [f"ACC{i}" for i in range(101, 111)],
        "Amount": np.random.uniform(10, 5000, 10),
        "Transaction Date": pd.date_range(start="2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d"),
        "Currency Code": ["USD" for _ in range(10)],
    }

    df = pd.DataFrame(data)

    # Apply trailing or leading spaces based on type
    if space_type == "leading":
        df = df.astype(str).apply(lambda x: x.map(lambda v: f"  {v}"))
    elif space_type == "trailing":
        df = df.astype(str).apply(lambda x: x.map(lambda v: f"{v}  "))
    elif space_type == "mixed":
        df = df.astype(str).apply(lambda x: x.map(lambda v: f"  {v}  "))

    file_path = os.path.join(SAVE_DIR, file_name)
    df.to_excel(file_path, index=False, engine="openpyxl")
    print(f"✅ File {file_name} generated successfully with {severity} severity.")

# ✅ Generate test files for trailing spaces detection
trailing_spaces_files = {
    "transactions_trailing_spaces.csv": "High",
    "transactions_leading_spaces.xlsx": "Medium",
    "transactions_mixed_spaces.csv": "Low",
}

for file_name, severity in trailing_spaces_files.items():
    space_type = "trailing" if "trailing" in file_name else "leading" if "leading" in file_name else "mixed"
    if file_name.endswith(".csv"):
        create_csv_with_spaces(file_name, severity, space_type)
    else:
        create_excel_with_spaces(file_name, severity, space_type)

# ✅ Generate error handling test cases
error_handling_files = {
    "transactions_spaces.csv": ("Account Number", 5),
    "transactions_padded.xlsx": ("Currency Code", 3),
    "transactions_extra_spaces.csv": ("Transaction ID", 10),
}

for file_name, (column_name, threshold) in error_handling_files.items():
    space_type = "mixed"
    if file_name.endswith(".csv"):
        create_csv_with_spaces(file_name, f"Threshold {threshold}", space_type)
    else:
        create_excel_with_spaces(file_name, f"Threshold {threshold}", space_type)

# ✅ Generate batch processing test cases
batch_processing_files = ["batch_high_spaces.csv", "batch_medium_spaces.xlsx", "batch_low_spaces.csv"]

for file_name in batch_processing_files:
    if file_name.endswith(".csv"):
        create_csv_with_spaces(file_name, "Batch Processing", "mixed")
    else:
        create_excel_with_spaces(file_name, "Batch Processing", "mixed")

# ✅ Generate performance testing files (simulate large dataset)
def create_large_spaces_file(file_name, row_count, severity):
    """Generate a large dataset for performance testing."""
    data = {
        "Transaction ID": np.arange(1, row_count + 1),
        "Account Number": [f"ACC{i}" for i in range(1, row_count + 1)],
        "Amount": np.random.uniform(10, 5000, row_count),
        "Transaction Date": pd.date_range(start="2024-01-01", periods=row_count, freq="D").strftime("%Y-%m-%d"),
        "Currency Code": ["USD"] * row_count,
    }

    df = pd.DataFrame(data).astype(str).apply(lambda x: x.map(lambda v: f"  {v}  "))

    file_path = os.path.join(SAVE_DIR, file_name)

    if file_name.endswith(".csv"):
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False, engine="openpyxl")

    print(f"✅ Large file {file_name} generated successfully with {severity} severity.")

# ✅ Create performance test files
create_large_spaces_file("performance_2015_2020.csv", 100, "High")
create_large_spaces_file("performance_2021_2023.xlsx", 500, "Medium")

# ✅ Generate delimiter consistency test cases
delimiter_files = ["transactions_trailing_delimiters.csv", "transactions_extra_spaces_delim.csv"]

for file_name in delimiter_files:
    create_csv_with_spaces(file_name, "Delimiter Handling", "mixed")

print("\n🎉 All trailing spaces validation test files generated successfully!")
