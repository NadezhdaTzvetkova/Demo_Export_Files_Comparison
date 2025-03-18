import os
import pandas as pd
import numpy as np

# ✅ Ensure the save directory exists
SAVE_DIR = "test_data/generated_files"
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Define extra column structures
extra_column_formats = {
    "transactions_extra.csv": ["Transaction_ID", "Amount", "Transaction_Date", "Customer_Name", "Extra_Column1",
                               "Extra_Column2"],
    "transactions_extra.xlsx": ["Transaction_ID", "Amount", "Transaction_Date", "Customer_Name", "Extra_Column1",
                                "Extra_Column2"],
    "batch_extra.csv": ["Transaction_ID", "Amount", "Transaction_Date", "Status", "Extra_Column"],
    "transactions_2019.csv": ["Transaction_ID", "Amount", "Transaction_Date", "Unexpected_Field"],
    "transactions_2021.xlsx": ["Transaction_Code", "Transaction_Date", "Unknown_Column"],
    "performance_2015_2020.csv": ["Transaction_ID", "Amount", "Transaction_Date", "Status", "Extra_Column"],
    "performance_2021_2023.parquet": ["Transaction_ID", "Amount", "Transaction_Date", "Status", "Extra_Column"],
}


# ✅ Generate test data based on extra columns
def generate_test_file(file_name, columns):
    """ Generate and save a test file with the given column format """
    row_count = 100 if "performance" not in file_name else 500  # More rows for performance testing

    data = {
        "Transaction_ID": np.arange(1000, 1000 + row_count) if "Transaction_ID" in columns else None,
        "Amount": np.random.uniform(10, 5000, row_count).round(2) if "Amount" in columns else None,
        "Transaction_Date": pd.date_range(start="2022-01-01", periods=row_count,
                                          freq="D") if "Transaction_Date" in columns else None,
        "Customer_Name": ["John Doe", "Jane Smith", "Alice Brown", "Bob Martin"] * (
                    row_count // 4) if "Customer_Name" in columns else None,
        "Transaction_Code": ["T" + str(i) + "XYZ" for i in range(row_count)] if "Transaction_Code" in columns else None,
        "Reference": ["Ref-" + str(i).zfill(4) for i in range(row_count)] if "Reference" in columns else None,
        "Status": ["Completed", "Pending", "Failed", "Completed"] * (row_count // 4) if "Status" in columns else None,
        "Extra_Column1": ["ExtraData1"] * row_count if "Extra_Column1" in columns else None,
        "Extra_Column2": ["ExtraData2"] * row_count if "Extra_Column2" in columns else None,
        "Extra_Column": ["ExtraInfo"] * row_count if "Extra_Column" in columns else None,
        "Unexpected_Field": ["#ERROR", "@INVALID", "$FAIL", "&CORRUPT"] * (
                    row_count // 4) if "Unexpected_Field" in columns else None,
        "Unknown_Column": ["UNKNOWN_" + str(i) for i in range(row_count)] if "Unknown_Column" in columns else None,
    }

    df = pd.DataFrame({col: data[col] for col in columns if data[col] is not None})

    file_path = os.path.join(SAVE_DIR, file_name)

    if file_name.endswith(".csv"):
        df.to_csv(file_path, index=False)
    elif file_name.endswith(".xlsx"):
        df.to_excel(file_path, index=False, engine="openpyxl")
    elif file_name.endswith(".parquet"):
        try:
            import pyarrow  # Ensure pyarrow is installed
            df.to_parquet(file_path, index=False, engine="pyarrow")
        except ImportError:
            print(f"⚠️ Warning: Skipping Parquet file `{file_name}` because `pyarrow` is not installed.")

    print(f"✅ File {file_name} generated successfully.")


# ✅ Generate all test files
for file_name, columns in extra_column_formats.items():
    generate_test_file(file_name, columns)

print("\n🎉 All extra columns test files generated successfully!")
