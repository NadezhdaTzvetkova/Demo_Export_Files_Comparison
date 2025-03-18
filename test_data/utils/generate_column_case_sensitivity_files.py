import pandas as pd
import numpy as np

# Install dependencies if missing
try:
    import pyarrow
    import openpyxl
except ImportError:
    print("❌ Missing required libraries. Install them using:")
    print("   pip install pyarrow openpyxl pandas")
    exit(1)

# Define test files
test_files = [
    ("transactions_lower.csv", "lowercase"),
    ("transactions_UPPER.xlsx", "uppercase"),
    ("transactions_MiXeD.csv", "mixed_case"),
    ("database_expected_title_case.csv", "Title Case"),
    ("database_expected_lower_case.csv", "Lowercase"),
    ("batch_lowercase.csv", "lowercase"),
    ("batch_uppercase.csv", "uppercase"),
    ("batch_mixed_case.csv", "mixed_case"),
    ("transactions_2019.csv", "missing_column"),
    ("transactions_2021.xlsx", "unrecognized_column"),
    ("performance_2015_2020.csv", "performance"),
    ("performance_2021_2023.parquet", "performance"),
]

EXCEL_MAX_ROWS = 1_048_576


def generate_test_file(file_name, case_format):
    """Generate test data for column case sensitivity scenarios."""

    # Define column variations
    column_variants = {
        "lowercase": ["transaction_id", "amount", "currency", "timestamp", "status"],
        "uppercase": ["TRANSACTION_ID", "AMOUNT", "CURRENCY", "TIMESTAMP", "STATUS"],
        "mixed_case": ["Transaction_ID", "AMount", "Currency", "TimeStamp", "StatUS"],
        "Title Case": ["Transaction Id", "Amount", "Currency", "Timestamp", "Status"],
        "Lowercase": ["transaction_id", "amount", "currency", "timestamp", "status"],
        "missing_column": ["Transaction_ID", "Amount", "Currency", "Timestamp"],  # Missing 'Status'
        "unrecognized_column": ["Transaction_ID", "Amount", "Currency", "Timestamp", "Unknown_Column"],
    }

    # Create sample transaction data
    data = {
        "transaction_id": range(1, 101),  # 100 transactions
        "amount": [round(x * 1.5, 2) for x in range(1, 101)],
        "currency": ["USD", "EUR", "GBP", "USD", "EUR"] * 20,
        "timestamp": pd.date_range(start="2022-01-01", periods=100, freq="h"),  # ✅ Fixed warning
        "status": ["Completed", "Pending", "Failed", "Completed", "Pending"] * 20,
    }

    if case_format in column_variants:
        columns = column_variants[case_format]
    else:
        columns = ["Transaction_ID", "Amount", "Currency", "Timestamp", "Status"]

    df = pd.DataFrame(data)

    # ✅ Fix for column length mismatch
    df = df.iloc[:, :len(columns)]  # Ensure correct column count
    df.columns = columns  # Assign column names safely

    # Save CSV files
    if file_name.endswith(".csv"):
        df.to_csv(file_name, index=False)
        print(f"✅ File {file_name} generated successfully.")

    # Save Excel files
    elif file_name.endswith(".xlsx"):
        with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
            sheet_count = 1
            for start_row in range(0, len(df), EXCEL_MAX_ROWS):
                end_row = min(start_row + EXCEL_MAX_ROWS, len(df))
                sheet_name = f"Sheet_{sheet_count}"

                subset = df.iloc[start_row:end_row].copy()
                subset.reset_index(drop=True, inplace=True)

                subset.to_excel(writer, index=False, sheet_name=sheet_name)
                sheet_count += 1

        print(f"✅ File {file_name} generated successfully with {sheet_count - 1} sheets.")

    # Save Parquet files for performance testing
    elif file_name.endswith(".parquet"):
        df.to_parquet(file_name, index=False, engine="pyarrow")
        print(f"✅ File {file_name} generated successfully as a Parquet file.")


# Generate all test files
for file_info in test_files:
    generate_test_file(file_info[0], file_info[1])

print("\n🎉 All column case sensitivity test files generated successfully!")
